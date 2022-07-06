"""Application state store."""
import collections
from typing import Mapping

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


class AppState(CardState):
    """Application state store."""

    song_table_index: int = 0  # the current id
    sample_tree_index: str = ""  # the path of the current item

    def from_card(self, card: DelugeCardFS) -> 'AppState':
        """Increment song index."""
        self.set_card(card)
        self.set_songs({str(song.path.relative_to(card.card_root)): song for song in card.songs()})
        self.set_samples({str(sample.path.relative_to(card.card_root)): sample for sample in card.samples()})
        self.set_synths({str(synth.path.relative_to(card.card_root)): synth for synth in card.synths()})
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
