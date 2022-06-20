"""Card views."""

import operator

import PySimpleGUI as sg
from config import FONT_MED, FONT_LRG
from settings_window import get_theme

theme = get_theme()
if not theme:
    theme = sg.OFFICIAL_PYSIMPLEGUI_THEME

sg.theme(theme)

# Base64 versions of images of a folder and a file. PNG files (may not work with PySimpleGUI27, swap with GIFs)

folder_icon = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsSAAALEgHS3X78AAABnUlEQVQ4y8WSv2rUQRSFv7vZgJFFsQg2EkWb4AvEJ8hqKVilSmFn3iNvIAp21oIW9haihBRKiqwElMVsIJjNrprsOr/5dyzml3UhEQIWHhjmcpn7zblw4B9lJ8Xag9mlmQb3AJzX3tOX8Tngzg349q7t5xcfzpKGhOFHnjx+9qLTzW8wsmFTL2Gzk7Y2O/k9kCbtwUZbV+Zvo8Md3PALrjoiqsKSR9ljpAJpwOsNtlfXfRvoNU8Arr/NsVo0ry5z4dZN5hoGqEzYDChBOoKwS/vSq0XW3y5NAI/uN1cvLqzQur4MCpBGEEd1PQDfQ74HYR+LfeQOAOYAmgAmbly+dgfid5CHPIKqC74L8RDyGPIYy7+QQjFWa7ICsQ8SpB/IfcJSDVMAJUwJkYDMNOEPIBxA/gnuMyYPijXAI3lMse7FGnIKsIuqrxgRSeXOoYZUCI8pIKW/OHA7kD2YYcpAKgM5ABXk4qSsdJaDOMCsgTIYAlL5TQFTyUIZDmev0N/bnwqnylEBQS45UKnHx/lUlFvA3fo+jwR8ALb47/oNma38cuqiJ9AAAAAASUVORK5CYII='
file_icon = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsSAAALEgHS3X78AAABU0lEQVQ4y52TzStEURiHn/ecc6XG54JSdlMkNhYWsiILS0lsJaUsLW2Mv8CfIDtr2VtbY4GUEvmIZnKbZsY977Uwt2HcyW1+dTZvt6fn9557BGB+aaNQKBR2ifkbgWR+cX13ubO1svz++niVTA1ArDHDg91UahHFsMxbKWycYsjze4muTsP64vT43v7hSf/A0FgdjQPQWAmco68nB+T+SFSqNUQgcIbN1bn8Z3RwvL22MAvcu8TACFgrpMVZ4aUYcn77BMDkxGgemAGOHIBXxRjBWZMKoCPA2h6qEUSRR2MF6GxUUMUaIUgBCNTnAcm3H2G5YQfgvccYIXAtDH7FoKq/AaqKlbrBj2trFVXfBPAea4SOIIsBeN9kkCwxsNkAqRWy7+B7Z00G3xVc2wZeMSI4S7sVYkSk5Z/4PyBWROqvox3A28PN2cjUwinQC9QyckKALxj4kv2auK0xAAAAAElFTkSuQmCC'

def layout_sample_info():
    """Elements for Sample layout."""  
    view_sample = [
        [
            sg.Frame(
                "Samples",
                key="-SAMPLE-INFO-FRAME-",
                layout=[
                    [
                        sg.Text('', key='-SAMPLE-INFO-NAME-', font=FONT_LRG, size=(50,)),
                    ],
                    # [
                    #     sg.Text('Scale', font=FONT_MED, size=(10,)),
                    #     sg.Text('', key='-SAMPLE-INFO-SCALE-', font=FONT_MED, size=(10,)),
                    #     sg.Text('Tempo', font=FONT_MED, size=(10,)),
                    #     sg.Text('', key='-SAMPLE-INFO-TEMPO-', font=FONT_MED, size=(10,)),
                    # ],
                    # [
                    #     sg.Text('Min Firmware', font=FONT_MED, size=(10,)),
                    #     sg.Text(key="-SAMPLE-INFO-MIN-FW-", font=FONT_MED, size=(10,)),
                    #     # sg.B("BUTTON")
                    # ],
                ],
            )
        ]
    ]
    return view_sample


def sample_tree_data(samples):
    """Take a DFS Samples iterable, and return a tree..."""
    treedata = sg.TreeData()
    treedata.Insert('', 'SAMPLES', "SAMPLES", values=[], icon=folder_icon)
    # for s in samples:
    #     if sample.path
    #     # print(dir(s))
    #     data.append([s.path.name, s.scale(), s.tempo(), len(list(s.samples())), s.minimum_firmware()])
    return treedata

def add_files_in_folder(parent, dirname):
    files = os.listdir(dirname)
    for f in files:
        fullname = os.path.join(dirname, f)
        if os.path.isdir(fullname):            # if it's a folder, add folder and recurse
            treedata.Insert(parent, fullname, f, values=[], icon=folder_icon)
            add_files_in_folder(fullname, fullname)
        else:
            treedata.Insert(parent, fullname, f, values=[os.stat(fullname).st_size], icon=file_icon)

# add_files_in_folder('', starting_path)


filter_tooltip = """Filter files\nEnter a string in box to narrow down the list of files.\n
    File list will update with list of files with string in filename."""

filter_layout = [
    [
        sg.Text('Filter (F2):', font=FONT_MED, size=(15,)),
        sg.Input(size=(25, 1), enable_events=True, key='-FILTER-', tooltip=filter_tooltip, font=FONT_MED),
        sg.T(size=(15, 1), k='-FILTER NUMBER-', font=FONT_MED),
    ]
]

def layout_sample_tree(default_values):
    """A layout a samples treem attributes."""
    headings = ['Name', 'Scale', 'BPM', 'Samples', "min version"]
    layout = [[
        sg.Tree(data=default_values,
           headings=['Size', ],
           auto_size_columns=True,
           select_mode=sg.TABLE_SELECT_MODE_EXTENDED,
           num_rows=20,
           col0_width=40,
           key='-SAMPLE-TREE-',
           show_expanded=False,
           enable_events=True,
           expand_x=True,
           expand_y=True,
           ),
        ]
    ]
    return layout
