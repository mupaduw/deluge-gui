"""Song views."""

import operator

import PySimpleGUI as sg

from .config import FONT_LRG, FONT_MED
from .settings_window import get_theme

theme = get_theme()
if not theme:
    theme = sg.OFFICIAL_PYSIMPLEGUI_THEME

sg.theme(theme)


def layout_song_info():
    """Elements for Card layout."""
    # data.append([s.path.name, s.scale(), s.tempo(), len(list(s.samples())), s.minimum_firmware()])

    view_song = [
        [
            sg.Frame(
                "Song",
                key="-SONG-INFO-FRAME-",
                layout=[
                    [
                        sg.Text('', key='-SONG-INFO-NAME-', font=FONT_LRG, size=(50,)),
                    ],
                    [
                        sg.Text('Scale', font=FONT_MED, size=(10,)),
                        sg.Text('', key='-SONG-INFO-SCALE-', font=FONT_MED, size=(10,)),
                        sg.Text('Tempo', font=FONT_MED, size=(10,)),
                        sg.Text('', key='-SONG-INFO-TEMPO-', font=FONT_MED, size=(10,)),
                    ],
                    [
                        sg.Text('Min Firmware', font=FONT_MED, size=(10,)),
                        sg.Text(key="-SONG-INFO-MIN-FW-", font=FONT_MED, size=(10,)),
                        sg.Text('Synths', font=FONT_MED, size=(10,)),
                        sg.Text(key="-SONG-INFO-SYNTHS-", font=FONT_MED, size=(10,)),
                        sg.Text('Kits', font=FONT_MED, size=(10,)),
                        sg.Text(key="-SONG-INFO-KITS-", font=FONT_MED, size=(10,)),
                    ],
                ],
            ),
        ],
        # [
        #     sg.HorizontalSeparator(color = None,
        #         pad = None,
        #         p = None,
        #         key = None,
        #         k = None),
        # ],
        [layout_song_samples()],  # -SONG-SAMPLES-TABLE-
    ]
    return view_song


def layout_song_samples():
    """List samples in the song."""
    headings = ['Path', 'Sample']
    layout = [
        [
            sg.Table(
                values=[],
                headings=headings,
                font=FONT_MED,
                # max_col_width=25,
                auto_size_columns=True,
                display_row_numbers=False,
                justification='left',
                num_rows=20,
                alternating_row_color='lightblue',
                key='-SONG-SAMPLES-TABLE-',
                selected_row_colors='black on yellow',
                enable_events=True,
                expand_x=True,
                expand_y=True,
                enable_click_events=True,  # Comment out to not enable header and other clicks
                # tooltip='This is a table',
            )
        ],
    ]
    return layout


def song_table_data(songs):
    """Take a DFS Songs iterable, and return a table with..."""
    # ['Name', 'BPM', "Path", "Samples"]
    # 'cardfs', 'minimum_firmware', 'mode_notes', 'path', 'root_elem', 'root_note', 'samples',
    # 'scale', 'scale_mode', 'tempo',
    data = []
    for s in songs:
        # print(dir(s))
        data.append([s.path.name, s.scale(), s.tempo(), len(list(s.samples())), s.minimum_firmware()])
    return data


def sort_table(table, cols):
    """Sort a table by multiple columns.

    table: a list of lists (or tuple of tuples) where each inner list
           represents a row
    cols:  a list (or tuple) specifying the column numbers to sort by
           e.g. (1,0) would sort by column 1, then by column 0
    """
    for col in reversed(cols):
        try:
            table = sorted(table, key=operator.itemgetter(col))
        except Exception as e:
            sg.popup_error('Error in sort_table', 'Exception in sort_table', e)
    return table


def layout_song_table():
    """A layout a table of song attributes."""
    headings = ['Name', 'Scale', 'BPM', 'Samples', "min version"]
    layout = [
        [
            sg.Table(
                values=[],
                headings=headings,
                font=FONT_MED,
                max_col_width=25,
                auto_size_columns=True,
                display_row_numbers=False,
                justification='center',
                num_rows=20,
                alternating_row_color='lightblue',
                key='-SONG-TABLE-',
                selected_row_colors='black on yellow',
                enable_events=True,
                expand_x=True,
                expand_y=True,
                enable_click_events=True,  # Comment out to not enable header and other clicks
                tooltip='This is a table',
            )
        ],
        [sg.Text('Cell clicked:'), sg.T(key='-SONG-CELL-CLICKED-')],
    ]
    return layout
