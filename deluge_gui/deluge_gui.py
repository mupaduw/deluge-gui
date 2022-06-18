"""Main module."""
import PySimpleGUI as sg
import os

APP_NAME = "Deluge GUI"

def get_demo_path():
    """
    Get the top-level folder path
    :return: Path to list of files using the user settings for this file.  Returns folder of this file if not found
    :rtype: str
    """
    demo_path = sg.user_settings_get_entry('-home folder-', os.path.join(os.path.dirname(__file__), 'demo_programs'))

    return demo_path

def get_theme():
    """
    Get the theme to use for the program
    Value is in this program's user settings. If none set, then use PySimpleGUI's global default theme
    :return: The theme
    :rtype: str
    """
    # First get the current global theme for PySimpleGUI to use if none has been set for this program
    try:
        global_theme = sg.theme_global()
    except:
        global_theme = sg.theme()
    # Get theme from user settings for this program.  Use global theme if no entry found
    user_theme = sg.user_settings_get_entry('-theme-', '')
    if user_theme == '':
        user_theme = global_theme
    return user_theme

def settings_window():
    """
    Show the settings window.
    This is where the folder paths and program paths are set.
    Returns True if settings were changed

    :return: True if settings were changed
    :rtype: (bool)
    """

    try:    # in case running with old version of PySimpleGUI that doesn't have a global PSG settings path
        global_theme = sg.theme_global()
    except:
        global_theme = ''

    layout = [[sg.T('Program Settings', font='DEFAULT 25')],
              [sg.T('Path to Deluge home folder',  font='_ 16')],
               [sg.Combo(sorted(sg.user_settings_get_entry('-home folder-', [])), 
                    default_value=sg.user_settings_get_entry('-home folder-', 
                        get_demo_path()), size=(50, 1), key='-HOMEFOLDER-'),
                    sg.FolderBrowse('Folder Browse', target='-HOMEFOLDER-')],
              [sg.T('Theme', font='_ 16')],
              [sg.T('Leave blank to use global default'), sg.T(global_theme)],
              [sg.Combo(['']+sg.theme_list(),sg.user_settings_get_entry('-theme-', ''), readonly=True,  k='-THEME-')],
              [sg.B('Ok', bind_return_key=True), sg.B('Cancel')],
              ]

    window = sg.Window('Settings', layout)

    settings_changed = False

    while True:
        event, values = window.read()
        if event in ('Cancel', sg.WIN_CLOSED):
            break
        if event == 'Ok':
            sg.user_settings_set_entry('-home folder-', values['-HOMEFOLDER-'])
            sg.user_settings_set_entry('-theme-', values['-THEME-'])
            settings_changed = True
            break
        elif event == 'Clear History':
            sg.user_settings_set_entry('-folder names-', [])
            sg.user_settings_set_entry('-last filename-', '')
            window['-FOLDERNAME-'].update(values=[], value='')

    window.close()
    return settings_changed





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
    # First the window layout...2 columns
    layout = [
              [sg.T(f'Hello From {APP_NAME}!'), sg.T('This is the shortest GUI program ever!')],
              [sg.B('Settings'), sg.Button('Exit')]]

    window = sg.Window(APP_NAME, layout, finalize=True)
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
