"""Window definitions and helper functions."""

import PySimpleGUI as sg

from .app_state import AppState, AppWindows
from .card_views import layout_card_info, select_card_control
from .config import APP_NAME, FONT_MED
from .kit_views import layout_kit_info, layout_kit_table
from .sample_views import layout_sample_info, layout_sample_tree
from .settings_window import get_theme
from .song_views import layout_song_info, layout_song_table
from .synth_views import layout_synth_info, layout_synth_table


def make_song_window(x: int, y: int) -> sg.Window:
    """Create the song window."""
    layout = [[layout_song_info()]]
    window = sg.Window(
        'Deluge Song', layout=None, location=(x, y), return_keyboard_events=True, resizable=True, finalize=True
    )
    window.layout(layout)
    window.finalize()
    window.hide()
    window.bind('<Up>', "+KB-UP+")
    window.bind('<Down>', "+KB-DN+")
    return window


def make_sample_window(x: int, y: int) -> sg.Window:
    """Create the sample window."""
    layout = [[layout_sample_info()]]
    window = sg.Window(
        'Deluge Sample', layout=None, location=(x, y), return_keyboard_events=True, resizable=True, finalize=True
    )
    window.layout(layout)
    window.finalize()
    window.hide()
    window.bind('<Up>', "+KB-UP+")
    window.bind('<Down>', "+KB-DN+")
    window.bind('<space>', "-PLAY-")
    return window


def make_kit_window(x: int, y: int) -> sg.Window:
    """Create the kit window."""
    layout = [[layout_kit_info()]]
    window = sg.Window(
        'Deluge Kit', layout=None, location=(x, y), return_keyboard_events=True, resizable=True, finalize=True
    )
    window.layout(layout)
    window.finalize()
    window.hide()
    window.bind('<Up>', "+KB-UP+")
    window.bind('<Down>', "+KB-DN+")
    window.bind('<space>', "-PLAY-")
    return window


def make_synth_window(x: int, y: int) -> sg.Window:
    """Create the synth window."""
    layout = [[layout_synth_info()]]
    window = sg.Window(
        'Deluge Synth', layout=None, location=(x, y), return_keyboard_events=True, resizable=True, finalize=True
    )
    window.layout(layout)
    window.finalize()
    window.hide()
    window.bind('<Up>', "+KB-UP+")
    window.bind('<Down>', "+KB-DN+")
    window.bind('<space>', "-PLAY-")
    return window


def make_main_window(card) -> sg.Window:
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
                                        layout_song_table(),
                                        expand_x=True,
                                        expand_y=True,
                                    ),
                                    sg.Tab(
                                        'Samples',
                                        layout_sample_tree(),
                                        expand_x=True,
                                        expand_y=True,
                                    ),
                                    sg.Tab(
                                        'Kits',
                                        layout_kit_table(),
                                        expand_x=True,
                                        expand_y=True,
                                    ),
                                    sg.Tab(
                                        'Synths',
                                        layout_synth_table(),
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
        [sg.B('Settings'), sg.Button('Exit'), sg.Sizegrip()],
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
    window.bind('<space>', "-PLAY-")

    # you can bind to elements too BUT these examples interfere with Table events :(...
    # window['-SONG-TABLE-'].bind('<Button-1>', '+CLICK-1+', True)
    # window['-SONG-TABLE-'].bind('<Button-2>', '+CLICK-2+', False)
    return window


def create_windows(state_store: AppState) -> AppWindows:
    """Define layout and create Windows."""
    window = make_main_window(state_store.card)
    loc = window.current_location()

    # draw song window with first song on card.
    song_window = make_song_window(loc[0] + window.size[0], loc[1])
    song_window.hide()

    # draw sample window with first sample on card.
    sample_window = make_sample_window(loc[0] + window.size[0], loc[1])
    sample_window.hide()

    # draw kit window with first kit on card.
    kit_window = make_kit_window(loc[0] + window.size[0], loc[1])
    kit_window.hide()

    # draw synth window with first synth on card.
    synth_window = make_synth_window(loc[0] + window.size[0], loc[1])
    synth_window.hide()

    # the ummutable list to pass around to event handlers
    return AppWindows(window, song_window, sample_window, kit_window, synth_window)


def close_windows(windows):
    """Dispose of all the windows."""
    windows.song.close()
    windows.sample.close()
    windows.kit.close()
    windows.main.close()
