"""Main module."""

from pathlib import Path

import PySimpleGUI as sg
from app_state import AppState
from deluge_card import DelugeCardFS
from event_handlers import do_card_list, do_play_sample, do_sample_tree, do_song_table, main_events_misc
from windows import close_windows, create_windows

if __name__ == '__main__':

    # set initial state
    state_store = AppState()

    card_path = sg.user_settings_get_entry('-CARD-INFO-PATH-', None)
    if card_path:
        print(card_path)
        card = DelugeCardFS(Path(card_path))  # [0] the selected card
        state_store = state_store.from_card(card)

    # create the windows
    windows = create_windows(state_store)

    # Send an event to fill the windows
    windows.main.write_event_value('-CARD LIST-', Path(card_path))

    # --------- setup event dispatch dictionaries -------
    dispatch_dict_main = {
        '-CARD LIST-': do_card_list,
        '-SAMPLE-TREE-': do_sample_tree,
        '-SONG-TABLE-': do_song_table,
        '-PLAY-': do_play_sample,
    }

    dispatch_dict_sample = {'-PLAY-': do_play_sample}

    while True:  # Event Loop

        event, values = windows.main.read(timeout=0)
        if not event == '__TIMEOUT__':
            print(f'event: {event}, values: {values}')

        if event in dispatch_dict_main:
            func = dispatch_dict_main[event]
            func(event, values, windows, state_store)

        if event in ('Exit', sg.WIN_CLOSED, sg.WINDOW_CLOSE_ATTEMPTED_EVENT):
            sg.user_settings_set_entry('-location-', windows.main.current_location())
            break

        main_events_misc(event, values, windows, state_store)

        #####
        ##
        ## SONG WINDOW EVENTS
        ##
        #####
        event, values = windows.song.read(timeout=0)
        if not event == '__TIMEOUT__':
            print(f'song window event: {event}, values: {values}')

        if event == '+KB-UP+':
            # Adds a key & value tuple to the queue that is used by threads to communicate with the window
            windows.main.write_event_value(
                '-SONG-TABLE-PREV-', {"-SONG-INFO-NAME-": windows.song["-SONG-INFO-NAME-"].get()}
            )

        if event == '+KB-DN+':
            # Adds a key & value tuple to the queue that is used by threads to communicate with the window
            windows.main.write_event_value(
                '-SONG-TABLE-NEXT-', {"-SONG-INFO-NAME-": windows.song["-SONG-INFO-NAME-"].get()}
            )

        #####
        ##
        ## SAMPLE WINDOW EVENTS
        ##
        #####
        event, values = windows.sample.read(timeout=0)
        if not event == '__TIMEOUT__':
            print(f'sample window event: {event}, values: {values}')

        if event in dispatch_dict_sample:
            func = dispatch_dict_sample[event]
            func(event, values, windows, state_store)


close_windows(windows)
