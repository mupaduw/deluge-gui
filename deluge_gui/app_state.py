"""Application state store."""
import collections
from typing import Mapping

from attr import define
from deluge_card import DelugeCardFS, DelugeKit, DelugeSong, DelugeSynth, Sample

Windows = collections.namedtuple('Windows', 'main, song, sample')


class CardState(object):
    """represents state of the card application.

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

    def set_samples(self, samples: Mapping[str, Sample]):
        """Set the samples mapping path -> object."""
        self.samples = samples
        return self

    def get_sample_id(self, idx: int) -> Sample:
        sample_key = list(self.samples.keys())[idx]
        return self.samples[sample_key]

    def set_songs(self, songs: Mapping[str, DelugeSong]):
        """Set the songs mapping path -> object."""
        self.songs = songs
        return self

    def get_song_id(self, idx: int) -> DelugeSong:
        song_key = list(self.songs.keys())[idx]
        return self.songs[song_key]

    def set_synths(self, synths: Mapping[str, DelugeSynth]):
        """Set the synths mapping path -> object."""
        self.synths = synths
        return self


class AppState(CardState):

    song_table_index: int = 0  # the current id

    def decr_song_table_index(self):
        if not self.song_table_index == 0:
            self.song_table_index -= 1
        return self.song_table_index

    def incr_song_table_index(self):
        if not self.song_table_index == len(self.songs) - 1:
            self.song_table_index += 1
        return self.song_table_index
