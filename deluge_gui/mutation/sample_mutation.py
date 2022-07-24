"""Sample mutation functions, wrappers for mutations available in deluge-card package."""
from pathlib import Path

from deluge_card import DelugeCardFS
from deluge_card.deluge_sample import validate_mv_dest

debug = True
verbose = True


def move_sample(card: DelugeCardFS, dest: str, pattern: str):
    """Use deluge-card to safely move samples, updating XML in Song, Kit and Synth files."""
    try:
        validate_mv_dest(card.card_root, Path(dest))
        new_path = Path(dest)
    except ValueError as err:
        print(err)
        return

    count = dict(move_file=0, update_song_xml=0, update_kit_xml=0, update_synth_xml=0)
    for modop in card.mv_samples(pattern, new_path):
        if debug:
            print(f'modop: {modop}')
        count[modop.operation] += 1
        if verbose:
            print(f"{str(modop.path)} {modop.operation}")

    return (
        f'moved {count["move_file"]} samples, in {count["update_song_xml"]} songs, '
        f'{count["update_kit_xml"]} kits, '
        f'{count["update_synth_xml"]} synths.'
    )
