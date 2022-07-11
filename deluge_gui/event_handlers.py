"""Event handler functions."""
import PySimpleGUI as sg
import sounddevice as sd
import soundfile as sf
from deluge_card import DelugeCardFS

from .app_state import AppState, AppWindows
from .card_views import get_cards_list
from .kit_views import kit_table_data
from .sample_views import sample_tree_data
from .settings_window import settings_window
from .song_views import song_table_data, sort_table
from .synth_views import synth_table_data
from .windows import close_windows


def do_play_sample(event: str, values: dict, windows: AppWindows, state_store: AppState):
    """Event handler for -PLAY-."""
    sample = state_store.get_sample_key(state_store.sample_tree_index)
    data, fs = sf.read(sample.path)
    sd.play(data, fs)


def do_card_list(event: str, values: dict, windows: AppWindows, state_store: AppState):
    """User changes the selected card."""
    card = DelugeCardFS(values['-CARD LIST-'])  # [0] the selected card
    state_store.from_card(card)

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
    window['-SAMPLE-TREE-'].update(values=sample_tree_data(state_store.card, state_store.samples.values()))
    window['-KIT-TABLE-'].update(values=kit_table_data(state_store.kits.values()))
    window['-SYNTH-TABLE-'].update(values=synth_table_data(state_store.synths.values()))


def do_song_table(event: str, values: dict, windows: AppWindows, state_store: AppState):
    """User changes the selected song."""
    print('do_song_table')
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
        '-SONG-INFO-SYNTHS-': len(list(song.synths)),
        '-SONG-INFO-KITS-': len(list(song.kits)),
        '-SONG-SAMPLES-TABLE-': [
            [s.path.relative_to(state_store.card.card_root).parent, s.path.name] for s in list(song.samples())
        ],
    }
    windows.song.fill(values_dict)
    windows.reveal_secondary(windows.song)


def do_sample_tree(event: str, values: dict, windows: AppWindows, state_store: AppState):
    """Event handler for when user selects a node in the sample tree."""
    if not values['-SAMPLE-TREE-']:  # handle header row click
        return
    # print(state_store.samples)
    if values['-SAMPLE-TREE-'][0][-3:].lower() == 'wav':
        # user selected a sample - yay
        state_store.sample_tree_index = values['-SAMPLE-TREE-'][0]
        # print(f'sample_tree_index: {state_store.sample_tree_index}')
    sample = state_store.get_sample_key(state_store.sample_tree_index)
    values_dict = {
        '-SAMPLE-INFO-NAME-': sample.path.name,
        '-SAMPLE-INFO-PATH-': sample.path.relative_to(state_store.card.card_root),
        '-SAMPLE-SETTINGS-TABLE-': [
            [ss.xml_file.path.relative_to(state_store.card.card_root), ss.xml_path] for ss in sample.settings
        ],
    }
    windows.sample.fill(values_dict)
    windows.reveal_secondary(windows.sample)


def do_kit_table(event: str, values: dict, windows: AppWindows, state_store: AppState):
    """User changes the selected kit."""
    print('do_kit_table')
    if not values['-KIT-TABLE-']:  # handle header row click
        return
    state_store.kit_table_index = values['-KIT-TABLE-'][0]
    kit = state_store.get_kit_id(values['-KIT-TABLE-'][0])
    print('XXX', kit)
    values_dict = {
        '-KIT-INFO-NAME-': kit.path.name,
        # '-SONG-SAMPLES-TABLE-': [
        #     [s.path.relative_to(state_store.card.card_root).parent, s.path.name] for s in list(song.samples())
        # ],
    }
    windows.kit.fill(values_dict)
    windows.reveal_secondary(windows.kit)


def do_synth_table(event: str, values: dict, windows: AppWindows, state_store: AppState):
    """User changes the selected synth."""
    print('do_synth_table')
    if not values['-SYNTH-TABLE-']:  # handle header row click
        return
    state_store.synth_table_index = values['-SYNTH-TABLE-'][0]
    synth = state_store.get_synth_id(values['-SYNTH-TABLE-'][0])
    print('XXX', synth)
    print(dir(synth))
    values_dict = {
        '-SYNTH-INFO-NAME-': synth.path.name,
        '-SYNTH-INFO-MODE-': synth.mode.value,
        '-SYNTH-INFO-POLYPHONY-': synth.polyphonic.value,
        '-SYNTH-INFO-LPFMODE-': synth.lpf_mode.value,
        '-SYNTH-INFO-MODFXTYPE-': synth.mod_fx_type.value,
        # '-SONG-SAMPLES-TABLE-': [
        #     [s.path.relative_to(state_store.card.card_root).parent, s.path.name] for s in list(song.samples())
        # ],
    }
    windows.synth.fill(values_dict)
    windows.reveal_secondary(windows.synth)


def main_events_misc(event: str, values: dict, windows: AppWindows, state_store: AppState):
    """Misc events for the main window."""
    if event == 'Settings':  # Open the User Settings Window.
        if settings_window() is True:
            close_windows(windows)

    if event == "Refresh Cards":  # Refresh button, maybe redundant?
        windows.main['-CARD LIST-'].update(values=[x.card_root for x in get_cards_list()])

    if isinstance(event, tuple):
        # TABLE CLICKED Event has value in format ('-TABLE-', '+CLICKED+', (row,col))
        if event[0] == '-SONG-TABLE-':
            # print(recvr, recvr.key, recvr.value)
            if event[2][0] == -1 and event[2][1] != -1:  # Header was clicked and wasn't the "row" column
                col_num_clicked = event[2][1]
                new_table = sort_table(song_table_data(state_store.songs.values()), (col_num_clicked, 0))
                windows.main['-SONG-TABLE-'].update(new_table)
                return
            else:
                print("unhandled song event 1")
            return
        if event[0] == '-KIT-TABLE-':
            # print(recvr, recvr.key, recvr.value)
            if event[2][0] == -1 and event[2][1] != -1:  # Header was clicked and wasn't the "row" column
                col_num_clicked = event[2][1]
                new_table = sort_table(kit_table_data(state_store.kits.values()), (col_num_clicked, 0))
                windows.main['-KIT-TABLE-'].update(new_table)
                return
            else:
                print("unhandled kit event 1")
            return
        if event[0] == '-SYNTH-TABLE-':
            # print(recvr, recvr.key, recvr.value)
            if event[2][0] == -1 and event[2][1] != -1:  # Header was clicked and wasn't the "row" column
                col_num_clicked = event[2][1]
                new_table = sort_table(synth_table_data(state_store.synths.values()), (col_num_clicked, 0))
                windows.main['-SYNTH-TABLE-'].update(new_table)
                return
            else:
                print("unhandled kit event 1")
            return
        else:
            print("unhandled event 2")

    if event == '-SONG-TABLE-PREV-':  # key press song_window
        windows.main['-SONG-TABLE-'].update(select_rows=[state_store.decr_song_table_index()])

    if event == '-SONG-TABLE-NEXT-':  # key press song_window
        windows.main['-SONG-TABLE-'].update(select_rows=[state_store.incr_song_table_index()])
