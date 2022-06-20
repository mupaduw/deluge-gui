"""Event dispatch andler functions."""
import PySimpleGUI as sg
from deluge_card import DelugeCardFS
from song_views import song_table_data


def do_card_list(event, values, window):
    """User changes the selected card."""
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
    print('** card info updated **')
