"""Main module."""

import collections
from pathlib import Path
from typing import Callable

import PySimpleGUI as sg
import simpleaudio as sa
from app_state import AppState, Windows
from card_views import get_cards_list, layout_card_info, select_card_control
from config import APP_NAME, FONT_MED
from deluge_card import DelugeCardFS
from event_handlers import do_card_list, do_song_table
from sample_views import layout_sample_info, layout_sample_tree, sample_tree_data
from settings_window import get_theme, settings_window
from song_views import layout_song_info, layout_song_table, song_table_data, sort_table

state_store = AppState()  # contains the entire application state


def play_sound(sample_path):
    """Start playing a wave file and return the player instance."""
    wave_obj = sa.WaveObject.from_wave_file(str(sample_path))
    play_obj = wave_obj.play()
    return play_obj

    # >>> wav.getparams()._fields
    # ('nchannels', 'sampwidth', 'framerate', 'nframes', 'comptype', 'compname')
    # >>> wav.getparams().framerate
    # 32000
    # >>> wav.getparams().compname
    # 'not compressed'
    # >>> wav.getparams().nframes
    # 79001
    # >>> wav.getparams().nframes/float(wav.getparams().framerate)
    # 2.46878125
    # >>> round(wav.getparams().nframes/float(wav.getparams().framerate), 3)
    # 2.469


def make_song_window(x: int, y: int) -> sg.Window:
    """Create the song window."""
    layout = [[layout_song_info()]]
    window = sg.Window('SONG', layout, location=(x, y), return_keyboard_events=True, resizable=True, finalize=True)
    window.bind('<Up>', "+KB-UP+")
    window.bind('<Down>', "+KB-DN+")
    return window


def make_sample_window(x: int, y: int) -> sg.Window:
    """Create the sample window."""
    layout = [[layout_sample_info()]]
    window = sg.Window('SAMPLE', layout, location=(x, y), return_keyboard_events=True, resizable=True, finalize=True)
    window.bind('<Up>', "+KB-UP+")
    window.bind('<Down>', "+KB-DN+")
    window.bind('<space>', "-PLAY-")
    return window


def main_window() -> sg.Window:
    """Create the main window."""
    theme = get_theme()
    if not theme:
        theme = sg.OFFICIAL_PYSIMPLEGUI_THEME
    sg.theme(theme)

    # OLD SKOOL TABS
    mainframe = (
        [
            sg.Frame(
                'Mainframe',
                expand_x=True,
                expand_y=True,
                layout=[
                    [
                        sg.TabGroup(
                            [
                                [
                                    sg.Tab(
                                        'Songs',
                                        layout_song_table(song_table_data(state_store.songs.values())),
                                        expand_x=True,
                                        expand_y=True,
                                    ),
                                    sg.Tab(
                                        'Samples',
                                        layout_sample_tree(sample_tree_data(card, state_store.samples.values())),
                                        expand_x=True,
                                        expand_y=True,
                                    ),
                                ]
                            ],
                            expand_x=True,
                            expand_y=True,
                            font=FONT_MED,
                        )
                    ]
                ],
            )
        ],
    )

    # First the window layout...2 columns
    layout = [
        select_card_control(card.card_root),
        layout_card_info(card),
        mainframe,
        [sg.B('Settings'), sg.B('PSG SDK'), sg.Button('Exit'), sg.Sizegrip()],
    ]

    location = sg.user_settings_get_entry('-location-')
    location = (0, 0) if location == [None, None] else location
    print(f'location {location}')
    window = sg.Window(
        APP_NAME,
        layout,
        resizable=True,
        finalize=True,
        return_keyboard_events=True,
        enable_close_attempted_event=True,
        location=location,
    )
    # for keybind strings see https://www.tcl.tk/man/tcl/TkCmd/keysyms.html
    # window.bind('<KeyPress>', "+KB-KEYPRESS+")
    # window.bind('<Up>', "+KB-UP+")
    # window.bind('<Down>', "+KB-DN+")
    # window.bind('<Shift_L>', "+KB-SHIFT_L+")
    # window.bind('<Shift_R>', "+KB-SHIFT_R+")

    # you can bind to elements too BUT these examples interfere with Table events :(...
    # window['-SONG-TABLE-'].bind('<Button-1>', '+CLICK-1+', True)
    # window['-SONG-TABLE-'].bind('<Button-2>', '+CLICK-2+', False)
    return window


#    #   ##   ### #    #
##  ##  #  #   #  ##   #
# ## # #    #  #  # #  #
# ## # ######  #  #  # #
#    # #    #  #  #   ##
#    # #    #  #  #    #
#    # #    # ### #    #

if __name__ == '__main__':

    # --------- A Dispatch Dictionary -------
    dispatch_dict = {
        '-CARD LIST-': do_card_list,
        # '-SAMPLE-TREE-': do_sample_tree
        '-SONG-TABLE-': do_song_table,
    }

    # --------- Set some initial state ------
    card_path = sg.user_settings_get_entry('-CARD-INFO-PATH-', None)
    if card_path:
        print(card_path)
        card = DelugeCardFS(Path(card_path))  # [0] the selected card
        # songs = list(card.songs())
        # samples = list(card.samples())
        state_store.set_card(card).set_songs(
            {str(song.path.relative_to(card.card_root)): song for song in card.songs()}
        ).set_samples({str(sample.path.relative_to(card.card_root)): sample for sample in card.samples()}).set_synths(
            {str(synth.path.relative_to(card.card_root)): synth for synth in card.synths()}
        ).set_kits(
            {str(kit.path.relative_to(card.card_root)): kit for kit in card.kits()}
        )

    print("Initial state", state_store.songs)
    player = None
    # song_table_index = 0

    # --------- Define layout and create Window -------
    window = main_window()
    loc = window.current_location()

    # draw song window with first song on card.
    song = state_store.get_song_id(0)
    song_window = make_song_window(loc[0] + window.size[0], loc[1])
    song_window.hide()

    # draw sample window with first sample on card.
    sample = state_store.get_sample_id(0)
    sample_window = make_sample_window(loc[0] + window.size[0], loc[1])
    sample_window.hide()

    # the ummutable list to pass around to event handlers
    windows = Windows(window, song_window, sample_window)

    while True:  # Event Loop

        event, values = window.read(timeout=0)
        if not event == '__TIMEOUT__':
            print(f'event: {event}, values: {values}')

        if event in dispatch_dict:  # Dispatch using a dispatch dictionary
            func = dispatch_dict[event]
            func(event, values, windows, state_store)

        if event in ('Exit', sg.WIN_CLOSED, sg.WINDOW_CLOSE_ATTEMPTED_EVENT):
            sg.user_settings_set_entry('-location-', windows.main.current_location())
            break

        if event == "PSG SDK":
            # ref https://raw.githubusercontent.com/PySimpleGUI/PySimpleGUI/master/PySimpleGUI.py
            sg.main_sdk_help()

        if event == 'Settings':  # Open the User Settings Window.
            if settings_window() is True:
                # Reset main_window to ensure new settings are applied.
                window.close()
                window = main_window()

        if event == "Refresh Cards":  # Refresh button, maybe redundant?
            window['-CARD LIST-'].update(values=[x.card_root for x in get_cards_list()])

        if isinstance(event, tuple):
            # TABLE CLICKED Event has value in format ('-TABLE-', '+CLICKED+', (row,col))
            if event[0] == '-SONG-TABLE-':
                # print(event)
                # recvr = window['-SONG-TABLE-'].get_previous_focus()
                # print(recvr, recvr.key, recvr.value)
                if event[2][0] == -1 and event[2][1] != -1:  # Header was clicked and wasn't the "row" column
                    col_num_clicked = event[2][1]
                    new_table = sort_table(song_table_data(state_store.songs.values()), (col_num_clicked, 0))
                    windows.main['-SONG-TABLE-'].update(new_table)
                    continue
                windows.main['-SONG-CELL-CLICKED-'].update(f'{event[2][0]},{event[2][1]}')
                # re-store Window 2
                song = state_store.get_song_id(event[2][0])
                values_dict = {
                    '-SONG-INFO-NAME': song.path.name,
                    '-SONG-INFO-SCALE': song.scale(),
                    '-SONG-INFO-TEMPO': song.tempo(),
                    '-SONG-INFO-MIN-FW': song.minimum_firmware(),
                }
                windows.song.fill(values_dict)
                windows.main['-SONG-INFO-FRAME-'].unhide_row()
                windows.main['-SAMPLE-INFO-FRAME-'].hide_row()
                # song_window.un_hide()

        if event == '-SONG-TABLE-PREV-':  # key press song_window
            # if not song_table_index == 0:
            #     song_table_index -= 1
            windows.main['-SONG-TABLE-'].update(select_rows=[state_store.decr_song_table_index()])

        if event == '-SONG-TABLE-NEXT-':  # key press song_window
            # if not song_table_index == len(state_store.songs) - 1:
            #     song_table_index += 1
            windows.main['-SONG-TABLE-'].update(select_rows=[state_store.incr_song_table_index()])

        if event == '-SAMPLE-TREE-':  # user changed value of selected sample
            if not values['-SAMPLE-TREE-']:  # handle header row click
                continue
            sample = samples[0] if not sample else sample
            values_dict = {
                '-SAMPLE-INFO-NAME-': sample.path.name,
                '-SAMPLE-INFO-PATH-': sample.path.relative_to(card.card_root),
                '-SAMPLE-SETTINGS-TABLE-': [
                    [ss.xml_file.path.relative_to(card.card_root), ss.xml_path] for ss in sample.settings
                ],
            }
            sample_window.fill(values_dict)
            # song_window['-SAMPLE-INFO-FRAME-'].update(visible=True)
            # song_window['-SONG-INFO-FRAME-'].update(visible=False)
            song_window.hide()
            sample_window.un_hide()

            # DEBUG
            # print(sample.settings[0].xml_file, sample.settings[0].xml_path)
            # print(dir(sample.settings[0].xml_file))

        #####
        ##
        ## SONG WINDOW EVENTS
        ##
        #####
        event, values = song_window.read(timeout=0)
        if not event == '__TIMEOUT__':
            print(f'song window event: {event}, values: {values}')

        if event == '+KB-UP+':
            # Adds a key & value tuple to the queue that is used by threads to communicate with the window
            window.write_event_value('-SONG-TABLE-PREV-', {"-SONG-INFO-NAME-": song_window["-SONG-INFO-NAME-"].get()})

        if event == '+KB-DN+':
            # Adds a key & value tuple to the queue that is used by threads to communicate with the window
            window.write_event_value('-SONG-TABLE-NEXT-', {"-SONG-INFO-NAME-": song_window["-SONG-INFO-NAME-"].get()})

        #####
        ##
        ## SAMPLE WINDOW EVENTS
        ##
        #####
        event, values = sample_window.read(timeout=0)
        if not event == '__TIMEOUT__':
            print(f'sample window event: {event}, values: {values}')

        if event == '-PLAY-':
            if isinstance(player, sa.PlayObject):  # already playing
                if player.is_playing():
                    player.stop()
                player = None
                continue
            # play the sample
            player = play_sound(samples[0].path)

    song_window.close()
    sample_window.close()
    window.close()
