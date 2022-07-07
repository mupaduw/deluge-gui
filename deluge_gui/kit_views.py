"""Kit views."""

import PySimpleGUI as sg

from .config import FONT_LRG, FONT_MED
from .settings_window import get_theme

theme = get_theme()
if not theme:
    theme = sg.OFFICIAL_PYSIMPLEGUI_THEME

sg.theme(theme)


def layout_kit_info():
    """Elements for Kit layout."""
    view_kit = [
        [
            sg.Frame(
                "Kit",
                key="-KIT-INFO-FRAME-",
                layout=[
                    [
                        sg.Text('', key='-KIT-INFO-NAME-', font=FONT_LRG, size=(50,)),
                    ],
                    [
                        sg.Text('Deets', font=FONT_MED, size=(10,)),
                        # sg.Text('', key='-KIT-INFO-SCALE-', font=FONT_MED, size=(10,)),
                        # sg.Text('Tempo', font=FONT_MED, size=(10,)),
                        # sg.Text('', key='-KIT-INFO-TEMPO-', font=FONT_MED, size=(10,)),
                    ],
                ],
            ),
        ],
        [layout_kit_samples()],  # -KIT-SAMPLES-TABLE-
    ]
    return view_kit


def layout_kit_samples():
    """List samples in the kit."""
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
                key='-KIT-SAMPLES-TABLE-',
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


def kit_table_data(kits):
    """Take a DFS Kits iterable, and return a table with..."""
    # ['Name', ]
    data = []
    for k in kits:
        data.append([k.path.name])
    return data


def layout_kit_table():
    """A layout a table of kit attributes."""
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
                key='-KIT-TABLE-',
                selected_row_colors='black on yellow',
                enable_events=True,
                expand_x=True,
                expand_y=True,
                enable_click_events=True,  # Comment out to not enable header and other clicks
                tooltip='This is a table',
            )
        ],
        [sg.Text('Cell clicked:'), sg.T(key='-KIT-CELL-CLICKED-')],
    ]
    return layout
