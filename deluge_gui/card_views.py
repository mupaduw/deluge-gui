"""Card views."""

import PySimpleGUI as sg
from config import FONT_MED
from deluge_card import list_deluge_fs
from settings_window import get_theme

theme = get_theme()
if not theme:
    theme = sg.OFFICIAL_PYSIMPLEGUI_THEME

sg.theme(theme)


def get_cards_list(path: str = None):
    """Get a list of paths that are Deluge Folder Systems."""
    path = path or sg.user_settings_get_entry('-home folder-')
    return [card for card in list_deluge_fs(path)]


def select_card_control():
    """Card Selector."""
    return [
        [
            sg.Text('Card:', font=FONT_MED, size=(15,)),
            sg.Combo(
                values=[x.card_root for x in get_cards_list()],
                # select_mode=sg.SELECT_MODE_EXTENDED,
                # size=(30, 10),
                bind_return_key=True,
                key='-CARD LIST-',
                font=FONT_MED,
                enable_events=True,
            ),
            sg.B("Refresh Cards"),
        ],
    ]


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
