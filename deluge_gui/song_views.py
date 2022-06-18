"""Card views."""

import operator

import PySimpleGUI as sg
from config import FONT_MED
from settings_window import get_theme

theme = get_theme()
if not theme:
    theme = sg.OFFICIAL_PYSIMPLEGUI_THEME

sg.theme(theme)


def layout_card_info():
    """Elements for Card layout."""
    view_card = [
        [
            sg.Frame(
                "Card info",
                layout=[
                    [
                        sg.Text('Path:', font=FONT_MED, size=(10,)),
                        sg.Text("", font=FONT_MED, size=(50,), key="-CARD-INFO-PATH-"),
                    ],
                    [
                        sg.Text('Songs:', font=FONT_MED, size=(10,)),
                        sg.Text("", font=FONT_MED, size=(10,), key="-CARD-INFO-SONGS-"),
                        sg.Text('Samples:', font=FONT_MED, size=(10,)),
                        sg.Text("", font=FONT_MED, size=(10,), key="-CARD-INFO-SAMPLES-"),
                    ],
                    [
                        sg.Text('Synths:', font=FONT_MED, size=(10,)),
                        sg.Text("", font=FONT_MED, size=(10,), key="-CARD-INFO-SYNTHS-"),
                        sg.Text('Kits:', font=FONT_MED, size=(10,)),
                        sg.Text("", font=FONT_MED, size=(10,), key="-CARD-INFO-KITS-"),
                    ],
                    # [
                    #     sg.Listbox(
                    #         values=[],
                    #         select_mode=sg.SELECT_MODE_EXTENDED,
                    #         size=(50, 25),
                    #         bind_return_key=True,
                    #         key='-CARD DETAIL-',
                    #         font=FONT_MED,
                    #     )
                    # ],
                ],
            )
        ]
    ]
    return [[sg.Col(view_card, vertical_alignment='t')]]


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


def layout_song_table(default_values):
    """A layout a table of song attributes."""
    headings = ['Name', 'Scale', 'BPM', 'Samples', "min version"]

    layout = [
        [
            sg.Table(
                values=default_values,
                headings=headings,
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
