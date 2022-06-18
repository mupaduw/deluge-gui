"""Main module."""

import PySimpleGUI as sg
from card_views import get_cards_list, layout_card_info, select_card_control
from config import APP_NAME, FONT_LRG, FONT_MED
from deluge_card import DelugeCardFS
from settings_window import get_theme, settings_window
from song_views import layout_song_table, song_table_data, sort_table
from pathlib import Path


def second_window(x, y):
    """Create a secondart (Song, Sample, Kit, Synth) window."""
    layout = [[sg.Text(f'Window 2\nlocation=({x}, {y})')], [sg.Button('Exit')]]

    window = sg.Window('Window 2', layout, location=(x, y), resizable=True, finalize=True)
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
        [sg.T(f'Hello From {APP_NAME}!', font=FONT_LRG), sg.T('This is the shortest GUI program ever!', font=FONT_MED)],
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
        APP_NAME, layout, resizable=True, finalize=True, enable_close_attempted_event=True, location=location
    )
    window.bring_to_front()

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

    window = main_window()
    loc = window.current_location()
    window_2 = second_window(loc[0] + window.size[0], loc[1])
    window_2.disappear()

    while True:  # Event Loop
        event, values = window.read()
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
                loc = window.current_location()
                window_2.close()
                window_2 = second_window(loc[0] + window.size[0], loc[1])


window.close()
