"""Event dispatch handler functions."""
import PySimpleGUI as sg
from app_state import AppState, Windows
from deluge_card import DelugeCardFS
from song_views import song_table_data


def do_card_list(event: str, values: dict, windows: Windows, state_store: AppState):
    """User changes the selected card."""
    card = DelugeCardFS(values['-CARD LIST-'])  # [0] the selected card

    # update state from deluge_card API
    state_store.set_card(card).set_songs(
        {str(song.path.relative_to(card.card_root)): song for song in card.songs()}
    ).set_samples({str(sample.path.relative_to(card.card_root)): sample for sample in card.samples()}).set_synths(
        {str(synth.path.relative_to(card.card_root)): synth for synth in card.synths()}
    ).set_kits(
        {str(kit.path.relative_to(card.card_root)): kit for kit in card.kits()}
    )

    # update UI Elements with new state
    window = windows.main
    window["-CARD-INFO-PATH-"].update(value=state_store.card.card_root)
    window["-CARD-INFO-SONGS-"].update(value=len(state_store.songs))
    window["-CARD-INFO-SAMPLES-"].update(value=len(state_store.samples))
    window["-CARD-INFO-SYNTHS-"].update(value=len(state_store.synths))
    window["-CARD-INFO-KITS-"].update(len(state_store.kits))
    window['-SONG-TABLE-'].update(values=song_table_data(state_store.songs.values()))

    # update the user_settings
    sg.user_settings_set_entry('-CARD-INFO-PATH-', str(card.card_root))
    # print('** card info updated **')


def do_song_table(event: str, values: dict, windows: Windows, state_store: AppState):
    """User changes the selected song."""
    if not values['-SONG-TABLE-']:  # handle header row click
        return
    state_store.song_table_index = values['-SONG-TABLE-'][0]
    song = state_store.get_song_id(values['-SONG-TABLE-'][0])
    print('XXX', song)
    values_dict = {
        '-SONG-INFO-NAME-': song.path.name,
        '-SONG-INFO-SCALE-': song.scale(),
        '-SONG-INFO-TEMPO-': song.tempo(),
        '-SONG-INFO-MIN-FW-': song.minimum_firmware(),
        '-SONG-SAMPLES-TABLE-': [
            [s.path.relative_to(state_store.card.card_root).parent, s.path.name] for s in list(song.samples())
        ],
    }
    windows.song.fill(values_dict)
    windows.sample.hide()
    windows.song.un_hide()
