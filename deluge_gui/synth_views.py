"""Synth views."""

import PySimpleGUI as sg

from .config import FONT_LRG, FONT_MED

# from .settings_window import get_theme

# theme = get_theme()
# if not theme:
#     theme = sg.OFFICIAL_PYSIMPLEGUI_THEME

# sg.theme(theme)


def layout_synth_info():
    """Elements for Synth layout."""
    view_synth = [
        [
            sg.Frame(
                "Synth",
                key="-SYNTH-INFO-FRAME-",
                layout=[
                    [
                        sg.Text('', key='-SYNTH-INFO-NAME-', font=FONT_LRG, size=(50,)),
                    ],
                    [
                        sg.Text('Mode', font=FONT_MED, size=(10,)),
                        sg.Text('', key='-SYNTH-INFO-MODE-', font=FONT_MED, size=(10,)),
                        sg.Text('Polyphony', font=FONT_MED, size=(10,)),
                        sg.Text('', key='-SYNTH-INFO-POLYPHONY-', font=FONT_MED, size=(10,)),
                        sg.Text('LPF mode', font=FONT_MED, size=(10,)),
                        sg.Text('', key='-SYNTH-INFO-LPFMODE-', font=FONT_MED, size=(10,)),
                    ],
                    [
                        sg.Text('Mod FX type', font=FONT_MED, size=(10,)),
                        sg.Text('', key='-SYNTH-INFO-MODFXTYPE-', font=FONT_MED, size=(10,)),
                    ],
                ],
            ),
        ],
        [layout_synth_samples()],  # -SYNTH-SAMPLES-TABLE-
    ]
    return view_synth


def layout_synth_samples():
    """List samples in the synth."""
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
                key='-SYNTH-SAMPLES-TABLE-',
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


def synth_table_data(synths):
    """Take a DFS Synths iterable, and return a table with..."""
    # ['Name', ]
    data = []
    for s in synths:
        data.append([s.path.name])
    return data


def layout_synth_table():
    """A layout a table of synth attributes."""
    headings = [
        'Name',
    ]
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
                key='-SYNTH-TABLE-',
                selected_row_colors='black on yellow',
                enable_events=True,
                expand_x=True,
                expand_y=True,
                enable_click_events=True,  # Comment out to not enable header and other clicks
                tooltip='This is a table',
            )
        ],
        [sg.Text('Cell clicked:'), sg.T(key='-SYNTH-CELL-CLICKED-')],
    ]
    return layout
