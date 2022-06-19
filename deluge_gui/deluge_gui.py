"""Main module."""

import PySimpleGUI as sg
from card_views import get_cards_list, layout_card_info, select_card_control
from config import APP_NAME, FONT_MED
from deluge_card import DelugeCardFS
from settings_window import get_theme, settings_window
from song_views import layout_song_table, song_table_data, sort_table, layout_song_info
from pathlib import Path


def second_window(song, x, y):
    """Create a secondart (Song, Sample, Kit, Synth) window."""
    layout = layout_song_info()
    window = sg.Window('Window 2', layout, location=(x, y), return_keyboard_events=True, resizable=True, finalize=True)
    # window.bind('<Click-1>', "+W2-CLICK-1+")
    # window.bind('<KeyPress>', "+W2-KP+")
    window.bind('<Up>', "+KB-UP+")
    window.bind('<Down>', "+KB-DN+")
    return window


def main_window():
    """Creates the main window.

    :return: The main window object
    :rtype: (sg.Window)
    """
    theme = get_theme()
    if not theme:
        theme = sg.OFFICIAL_PYSIMPLEGUI_THEME
    sg.theme(theme)

    #
    # filter_tooltip = """Filter files\nEnter a string in box to narrow down the list of files.\n
    #     File list will update with list of files with string in filename."""
    # filter_layout = [
    #     [
    #         sg.Text('Filter (F2):', font=FONT_MED, size=(15,)),
    #         sg.Input(size=(25, 1), enable_events=True, key='-FILTER-', tooltip=filter_tooltip, font=FONT_MED),
    #         sg.T(size=(15, 1), k='-FILTER NUMBER-', font=FONT_MED),
    #     ]
    # ]

    tab_layout_samples = [
        [
            sg.Listbox(
                values=[],
                select_mode=sg.SELECT_MODE_EXTENDED,
                size=(50, 25),
                bind_return_key=True,
                key='-SAMPLE LIST-',
                font=FONT_MED,
            )
        ]
    ]

    # OLD SKOOL TABS
    mainframe = (
        [
            sg.Frame(
                'Mainframe',
                expand_x=True,
                layout=[
                    [
                        sg.TabGroup(
                            [
                                [
                                    sg.Tab('Songs', layout_song_table(song_table_data(songs)), expand_x=True),
                                    sg.Tab('Samples', tab_layout_samples, expand_x=True),
                                ]
                            ],
                            expand_x=True,
                        )
                    ]
                ],
            )
        ],
    )

    # #BYO TABS uses  a vertical list of buttons and a multi-line text control
    # buttons = [[sg.B(e, pad=(0, 0), size=(22, 1), font='Courier 10')] for e in ['Cards', 'Songs']]
    # button_col = sg.Col(buttons, vertical_alignment='t')
    # pane_col =   sg.Col(layout_card_info(), vertical_alignment='t')
    # mline_col = sg.Col([[]])
    # # sg.Multiline(size=(100, 46), key='-ML-', write_only=True, reroute_stdout=True,
    # #.  font='Courier 10', expand_x=True, expand_y=True)],
    # #                     [sg.T(size=(80, 1), font='Courier 10 underline', k='-DOC LINK-', enable_events=True)]],
    # #  pad=(0, 0), expand_x=True, expand_y=True, vertical_alignment='t')
    # mainframe = [sg.Frame('Mainframe', layout=[[button_col, pane_col]])]

    # First the window layout...2 columns
    layout = [
        # filter_layout,
        select_card_control(card.card_root),
        layout_card_info(card),
        mainframe,
        [sg.B('Settings'), sg.B('PSG SDK'), sg.Button('Exit'), sg.Sizegrip()],
    ]

    # A new layout
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
    # window.bring_to_front()

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


if __name__ == '__main__':
    # Set some initial state ....
    card_path = sg.user_settings_get_entry('-CARD-INFO-PATH-', None)
    if card_path:
        print(card_path)
        card = DelugeCardFS(Path(card_path))  # [0] the selected card
        songs = list(card.songs())

    song_table_index = 0
    window = main_window()
    loc = window.current_location()

    # draw second window w first song on card.
    song = songs[0]
    window_2 = second_window(song, loc[0] + window.size[0], loc[1])
    window_2.hide()

    while True:  # Event Loop

        event, values = window.read(timeout=0)
        if not event == '__TIMEOUT__':
            print(f'event: {event}, values: {values}')

        if event in ('Exit', sg.WIN_CLOSED, sg.WINDOW_CLOSE_ATTEMPTED_EVENT):
            sg.user_settings_set_entry('-location-', window.current_location())
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

        if event == '-CARD LIST-':  # user changes value of selected card
            card = DelugeCardFS(values['-CARD LIST-'])  # [0] the selected card
            window["-CARD-INFO-PATH-"].update(value=card.card_root)
            sg.user_settings_set_entry('-CARD-INFO-PATH-', str(card.card_root))

            # get state from deluge_card API
            songs = list(card.songs())
            samples = list(card.samples())
            synths = list(card.synths())
            kits = list(card.kits())

            # update Elements with new state
            window["-CARD-INFO-SONGS-"].update(value=len(songs))
            window["-CARD-INFO-SAMPLES-"].update(value=len(samples))
            window["-CARD-INFO-SYNTHS-"].update(value=len(synths))
            window["-CARD-INFO-KITS-"].update(len(kits))
            window['-SONG-TABLE-'].update(values=song_table_data(songs))

        if isinstance(event, tuple):
            # TABLE CLICKED Event has value in format ('-TABLE-', '+CLICKED+', (row,col))
            if event[0] == '-SONG-TABLE-':
                # print(event)
                # recvr = window['-SONG-TABLE-'].get_previous_focus()
                # print(recvr, recvr.key, recvr.value)
                if event[2][0] == -1 and event[2][1] != -1:  # Header was clicked and wasn't the "row" column
                    col_num_clicked = event[2][1]
                    new_table = sort_table(song_table_data(songs), (col_num_clicked, 0))
                    window['-SONG-TABLE-'].update(new_table)
                    continue
                window['-SONG-CELL-CLICKED-'].update(f'{event[2][0]},{event[2][1]}')
                # re-store Window 2
                song = songs[event[2][0]]
                values_dict = {
                    '-SONG-INFO-NAME': song.path.name,
                    '-SONG-INFO-SCALE': song.scale(),
                    '-SONG-INFO-TEMPO': song.tempo(),
                    '-SONG-INFO-MIN-FW': song.minimum_firmware(),
                }
                window_2.fill(values_dict)
                # window_2.un_hide()

        if event == '-SONG-TABLE-PREV-':  # key press window_2
            if not song_table_index == 0:
                song_table_index -= 1
                window['-SONG-TABLE-'].update(select_rows=[song_table_index])

        if event == '-SONG-TABLE-NEXT-':  # key press window_2
            if not song_table_index == len(songs) - 1:
                song_table_index += 1
                window['-SONG-TABLE-'].update(select_rows=[song_table_index])

        if event == '-SONG-TABLE-':  # user changed value of selected song
            if not values['-SONG-TABLE-']:  # handle header row click
                continue
            loc = window.current_location()
            # window_2.close()
            # window_2 = second_window(
            #     song = songs[values['-SONG-TABLE-'][0]],
            #     x = loc[0] + window.size[0], y=loc[1])
            # window.force_focus()
            song_table_index = values['-SONG-TABLE-'][0]
            song = songs[song_table_index]
            values_dict = {
                '-SONG-INFO-NAME-': song.path.name,
                '-SONG-INFO-SCALE-': song.scale(),
                '-SONG-INFO-TEMPO-': song.tempo(),
                '-SONG-INFO-MIN-FW-': song.minimum_firmware(),
            }
            window_2.fill(values_dict)
            window_2.un_hide()

        event, values = window_2.read(timeout=0)
        if not event == '__TIMEOUT__':
            print(f'win 2 event: {event}, values: {values}')

        if event == '+KB-UP+':
            # Adds a key & value tuple to the queue that is used by threads to communicate with the window
            window.write_event_value('-SONG-TABLE-PREV-', {"-SONG-INFO-NAME-": window_2["-SONG-INFO-NAME-"].get()})

        if event == '+KB-DN+':
            # Adds a key & value tuple to the queue that is used by threads to communicate with the window
            window.write_event_value('-SONG-TABLE-NEXT-', {"-SONG-INFO-NAME-": window_2["-SONG-INFO-NAME-"].get()})

    window_2.close()
    window.close()
