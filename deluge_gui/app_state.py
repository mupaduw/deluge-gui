"""Application state store."""

from dataclasses import dataclass
from typing import Mapping

import PySimpleGUI as sg
from deluge_card import DelugeCardFS, DelugeKit, DelugeSong, DelugeSynth, DelugeSynthSound, Sample


@dataclass
class AppWindows:
    """Manage the application windows."""

    main: sg.Window
    song: sg.Window
    sample: sg.Window
    kit: sg.Window
    synth: sg.Window

    def reveal_secondary(self, activate: sg.Window):
        """Activate given window, hiding others."""
        secondaries = [self.song, self.sample, self.kit, self.synth]
        assert activate in secondaries
        secondaries.remove(activate)
        for w in secondaries:
            w.hide()
        activate.un_hide()


class CardState:
    """Represents state of the card.

    Attributes:
        card (DelugeCardFS): the deluge card.
        songs (Mapping[str, Song]): list of Songs (from the current card)
    """

    card: DelugeCardFS
    songs: Mapping[str, DelugeSong]
    song: str  # the current path
    samples: Mapping[str, Sample]
    sample: str  # the current path
    synths: Mapping[str, DelugeSynth]
    synth: str  # the current path
    kits: Mapping[str, DelugeKit]
    kit: str  # the current path

    def set_card(self, card):
        """Set the card object."""
        self.card = card
        return self

    def set_kits(self, kits: Mapping[str, DelugeKit]):
        """Set the kits mapping path -> object."""
        self.kits = kits
        return self

    def get_kit_id(self, idx: int) -> DelugeKit:
        """Get the kit identified by index."""
        kit_key = list(self.kits.keys())[idx]
        return self.kits[kit_key]

    def set_samples(self, samples: Mapping[str, Sample]):
        """Set the samples mapping path -> object."""
        self.samples = samples
        return self

    def get_sample_key(self, sample_key: str) -> Sample:
        """Get the sample identified by key (file path)."""
        # sample_key = list(self.samples.keys())[idx]
        return self.samples[sample_key]

    def set_songs(self, songs: Mapping[str, DelugeSong]):
        """Set the songs mapping path -> object."""
        self.songs = songs
        return self

    def get_song_id(self, idx: int) -> DelugeSong:
        """Get the song identified by index."""
        song_key = list(self.songs.keys())[idx]
        return self.songs[song_key]

    def set_synths(self, synths: Mapping[str, DelugeSynth]):
        """Set the synths mapping path -> object."""
        self.synths = synths
        return self

    def get_synth_id(self, idx: int) -> DelugeSynth:
        """Get the synth identified by index."""
        synth_key = list(self.synths.keys())[idx]
        return self.synths[synth_key]


class AppState(CardState):
    """Application state store."""

    song_table_index: int = 0  # the current id
    sample_tree_index: str = ""  # the path of the current item
    kit_table_index: int = 0  # the current id
    synth_table_index: int = 0  # the current id

    def from_card(self, card: DelugeCardFS) -> 'AppState':
        """Increment song index."""
        self.set_card(card)
        self.set_songs({str(song.path.relative_to(card.card_root)): song for song in card.songs()})
        self.set_samples({str(sample.path.relative_to(card.card_root)): sample for sample in card.samples()})
        self.set_synths(
            {str(synth.path.relative_to(card.card_root)): DelugeSynthSound.from_synth(synth) for synth in card.synths()}
        )
        # synths = {}
        # try:
        #     for synth in card.synths():
        #         synths[str(synth.path.relative_to(card.card_root))] = DelugeSynthSound.from_synth(synth)
        #     self.set_synths(synths)
        # except Exception as err:
        #     print('err', synth, synth.path)
        #     raise err
        self.set_kits({str(kit.path.relative_to(card.card_root)): kit for kit in card.kits()})
        self.sample_tree_index = list(self.samples.keys())[0]
        self.song_table_index = 0
        return self

    def decr_song_table_index(self) -> int:
        """Decrement song index."""
        if not self.song_table_index == 0:
            self.song_table_index -= 1
        return self.song_table_index

    def incr_song_table_index(self) -> int:
        """Increment song index."""
        if not self.song_table_index == len(self.songs) - 1:
            self.song_table_index += 1
        return self.song_table_index
