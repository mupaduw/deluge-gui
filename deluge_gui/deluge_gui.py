"""Main module."""

import PySimpleGUI as sg
from settings_window import settings_window, get_theme

APP_NAME = "Deluge GUI"
FONT_LRG = "_ 18"
FONT_MED = "_ 15"
FONT_SML = "_ 10"


def main_window():
    """
    Creates the main window
    :return: The main window object
    :rtype: (sg.Window)
    """
    theme = get_theme()
    if not theme:
        theme = sg.OFFICIAL_PYSIMPLEGUI_THEME
    sg.theme(theme)

    filter_tooltip = "Filter files\nEnter a string in box to narrow down the list of files.\nFile list will update with list of files with string in filename."
    filter_layout = [[sg.Text('Filter (F2):', font=FONT_MED), sg.Input(size=(25, 1), 
        enable_events=True, key='-FILTER-', tooltip=filter_tooltip, font=FONT_MED),
         sg.T(size=(15,1), k='-FILTER NUMBER-', font=FONT_MED)]]

    tab_layout_cards = [[sg.Listbox(values=[], select_mode=sg.SELECT_MODE_EXTENDED, size=(50,10), 
        bind_return_key=True, key='-CARD LIST-', font=FONT_MED)]]

    tab_layout_songs = [[sg.Listbox(values=[], select_mode=sg.SELECT_MODE_EXTENDED, size=(50,25), 
        bind_return_key=True, key='-SONG LIST-', font=FONT_MED)]]

    tab_layout_samples = [[sg.Listbox(values=[], select_mode=sg.SELECT_MODE_EXTENDED, size=(50,25), 
        bind_return_key=True, key='-SAMPLE LIST-', font=FONT_MED)]]

    # First the window layout...2 columns
    layout = [
        [sg.T(f'Hello From {APP_NAME}!', font=FONT_LRG), sg.T('This is the shortest GUI program ever!', font=FONT_MED)],
        filter_layout,
        [sg.Frame('Mainframe', 
            layout=[[sg.TabGroup([[
                    sg.Tab('Cards', tab_layout_cards), 
                    sg.Tab('Songs', tab_layout_songs),
                    sg.Tab('Samples', tab_layout_samples),
                    ]])
                    ]]
            )],
        [sg.B('Settings'), sg.Button('Exit')],
    ]

    window = sg.Window(APP_NAME, layout, resizable=True, finalize=True)
    window.bring_to_front()
    return window


if __name__ == '__main__':

    window = main_window()

    while True:  # Event Loop
        event, values = window.read()
        print(event, values)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Settings':
            if settings_window() is True:
                window.close()
                window = main_window()

window.close()
