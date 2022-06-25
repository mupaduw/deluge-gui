"""Sample views."""

from collections import defaultdict

import PySimpleGUI as sg

from .config import FONT_LRG, FONT_MED
from .settings_window import get_theme

theme = get_theme()
if not theme:
    theme = sg.OFFICIAL_PYSIMPLEGUI_THEME

sg.theme(theme)

# Base64 versions of images of a folder and a file. PNG files (may not work with PySimpleGUI27, swap with GIFs)

folder_icon = (
    b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsSAAALEgHS3X78AAABnUlEQVQ4y8WSv2rUQRSFv'
    b'7vZgJFFsQg2EkWb4AvEJ8hqKVilSmFn3iNvIAp21oIW9haihBRKiqwElMVsIJjNrprsOr/5dyzml3UhEQIWHhjmcpn7zblw4B9lJ8Xag9mlm'
    b'Qb3AJzX3tOX8Tngzg349q7t5xcfzpKGhOFHnjx+9qLTzW8wsmFTL2Gzk7Y2O/k9kCbtwUZbV+Zvo8Md3PALrjoiqsKSR9ljpAJpwOsNtlfXf'
    b'RvoNU8Arr/NsVo0ry5z4dZN5hoGqEzYDChBOoKwS/vSq0XW3y5NAI/uN1cvLqzQur4MCpBGEEd1PQDfQ74HYR+LfeQOAOYAmgAmbly+dgfid'
    b'5CHPIKqC74L8RDyGPIYy7+QQjFWa7ICsQ8SpB/IfcJSDVMAJUwJkYDMNOEPIBxA/gnuMyYPijXAI3lMse7FGnIKsIuqrxgRSeXOoYZUCI8pI'
    b'KW/OHA7kD2YYcpAKgM5ABXk4qSsdJaDOMCsgTIYAlL5TQFTyUIZDmev0N/bnwqnylEBQS45UKnHx/lUlFvA3fo+jwR8ALb47/oNma38cuqiJ'
    b'9AAAAAASUVORK5CYII='
)
file_icon = (
    b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsSAAALEgHS3X78AAABU0lEQVQ4y52TzStEURiHn/ec'
    b'c6XG54JSdlMkNhYWsiILS0lsJaUsLW2Mv8CfIDtr2VtbY4GUEvmIZnKbZsY977Uwt2HcyW1+dTZvt6fn9557BGB+aaNQKBR2ifkbgWR+cX13'
    b'ubO1svz++niVTA1ArDHDg91UahHFsMxbKWycYsjze4muTsP64vT43v7hSf/A0FgdjQPQWAmco68nB+T+SFSqNUQgcIbN1bn8Z3RwvL22MAvc'
    b'u8TACFgrpMVZ4aUYcn77BMDkxGgemAGOHIBXxRjBWZMKoCPA2h6qEUSRR2MF6GxUUMUaIUgBCNTnAcm3H2G5YQfgvccYIXAtDH7FoKq/AaqK'
    b'lbrBj2trFVXfBPAea4SOIIsBeN9kkCwxsNkAqRWy7+B7Z00G3xVc2wZeMSI4S7sVYkSk5Z/4PyBWROqvox3A28PN2cjUwinQC9QyckKALxj4'
    b'kv2auK0xAAAAAElFTkSuQmCC'
)

gs2 = (
    b'iVBORw0KGgoAAAANSUhEUgAAADgAAAA2CAYAAACSjFpuAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAc'
    b'dvqGQAAA7+SURBVGhDbZrLrmRHEUWzHve2zUseAAMQcz4CvoMBAyRgyoCvQUIIISZ8DxJTkGiQ7abb7oe776PqVBV77R1xzqlrVzsqIiMjM/'
    b'fOiMxTVdeby+UyfvWHX5wOm7fbzdgMv6Q2ku1WImOz0vZjby4YbjNq06Np0z/UT2dc0TLkHQxF87IWBv2X1mUzzig7NEv12ae3y7ls/CfsS/'
    b'VJPCKvb918Mv70m79tNr//y+8un3z3O+NnP/35eJgeFKB/EFEQREBlsHpVEwyZyH1tp29+0S7zSSOvTKlXk6sXYKPmGLf1thGLixbvvh6H7o'
    b'2IazP+8fzv48W7T8/b3diOn3z/JwK3Hfvtftzsdtb73X7s0IrYyXZbfbar/6bj9vQtgm+/vYnskBqzlnVcxbDeMj6617sxjpulvyRjhNlttO'
    b'LE5Yef/ECJOo+teCvF2pmhHFM7bLZ1S/svydBKz6LRHuNX+xknmdvfIF/rk6ttIUOn1KtvXkeopZHug0diZMt3Vv3Ks/XJYRDlmLOluCf2os'
    b'v/5Gx6FvdlRvvcTx8xS9y6n77M0f0Zf7W++4EaDJDAZ7MIsglNHD+aQMytz1O89Vpsu+l3I5P1hHNYT2xf5NJZL192WzvqXV1LKgf7fOWflA'
    b'FEtvUUPY62T5fjOJ0XmeSb0JLj+SB9sB/8W3aDRZjMgzX5ick80df1LEzOQi1afLpk4vhkS08rmxjbQyCkHb/WBc5g7X804KPGHs+x3X+ST2'
    b'1s95/Up/jYadNH1re80XE4P1imk6RsT8pgTx4//d130rjpIh9CW4AA1Rr/yYIvtv2Aq/7ErNqsMev4vTZ24TjahhA6scEJrrJFmNJ2Bp3aYu'
    b'1dALiFBSBBHyWAnd3OzjN5MjYpK8kOZCquMpV4YpYMWiq789juq3iPKX/WLjyFI3hTlial7MUX7Qxe9MZECVqTK2lyPfkKVAOmbw1qIVDgHF'
    b'tt9+ksdcyVhJBjvVEtauPvTXbmkLal3V9EpZczqLfJ7OlQcOmWDO5ywY7uxafK2EmxBmU5mMBZ/eeNBC0/EiKMKbvmyibhK71aK+ut43rDlz'
    b'KecRozvipRnjc0csaa2JLJLt1M0Atftw10UyBMIDJtkmFfLuUzcdtkUePZAGzGzxugseiaj3iTKN/RRNDgKEKF+4AfzOqrS2ajRqeeCQRGwU'
    b'h2Rz77q8+kAMXCXNvyszAikMlc9MWgA97+taZPG+A55jFlS/fG4A8uJHi8JmLMhb3ikOsS5amjRmfNGSRYC5mcdnXezSZsACE6AVbELcQZYD'
    b'QCyZlU9UUetTK6SJHtIuwNrHivrSwvFRIM8+ajNSbkwFQ+aR6AWz49kJmcN9KcR8CS+p5EIm3gtFmwQARA+rrsINYyBFwnXXLSrk76UCBber'
    b'gPcgiEM3bZjIfMX5UTQkUOP5ik50eF/MGvPiXNn4z4pJEySOaYzCVgYpGeuEvGi9u3agvURUT4FAJ4SFj0CaZli9/EsOXTjJCm7U8vXbJFMO'
    b'eUuUW81unKCGbZzhxYsMkkF1Aww80Z7DNIMOydOU1iPwNLPCkLYHshdjx2yi3ZCjEIiggiuyVEtbuKmX0iMmfWm6iMFdGsnfJN9aRtXGo3Ph'
    b'8ri7ALPzGaVPNDsEiR4hPpJtC7wqcMdBNmYEjR7tJy9gAJsRbAbxcSu8rafraJKfLbbkfGlkqoi8wbqDUtIWUMxlWEqh0eLfMlszzo3bEaNN'
    b's96WoBL67+CzslcpyxBggRZKdoa3343sm/gzDf0brfsZLVpvQGUeZsWs521gux2mz5nD3bEqqun4PEGFe+JZntFUHp7M51WWCbGOWDJnMqnS'
    b'ZnsAKOHfAioeyQsZ2IQXTfPmdNPuvEmKjGNUmfaa07rwfhsoMpJNdZo+1LRjoZ1BuDEqAB3gHI9SQllIh1kRa5oW8VvfOctTXJBg9wk0IXsR'
    b'uIijBtxzle49Xm3FK6vmVlo30WWdMkpYXDlxxYCl9XWThgs/G+RbX//rRyL+Y5h7l2IZrrt2s817LOpfRFbUqI8gzJ5eJIhiYRQGTvT+NWhG'
    b'6QIpq+yI6xjPPmsPMSz9uXVxHx+lWmVzh5PCwCQT5Xm6AzKLZ5REiKfWeRh+hSErKrZPI4gCBXPbsNyWTEGZS/SzIZu4igZDeite5eF9y+9M'
    b'6fGzkzfHk+z1n0Olqzb+kcFeHDnnFJTLQwOyF9yZigvhH3NwkF5MqtrNlOWXoBtBcsktJ+7rXIx2MgJSjwImR7x4ffe8lXin+j8/WF5nml6J'
    b'da76XWeKW5X0u/0zr3mpcjIKJq8ZzkC3dKLxlsXCZk3G2TwRD0c1Azzc7IEmTRZBEmycTspsuziKKdQZOLjHEnaJD4VMCfy34uUv/Rop9pW1'
    b'9Iv7RcRPB0+Z9Ifj7uT/8dd6d/j3fHf443krfHf42vjvJNX6j/g+bR+lq7cQRfjhAyl6cFbM6g8qDgdCpo/vaQHfEHbyZsrUWcQZPLVe6PWJ'
    b'f3muP1eDx/LvmvAH0q/yst8EHn7zQ+2m3Ht3e34+P97fjW9tn4ePdsPNvequ9m3O5uVLbS/FS4QfihgZ9RHjTXG5H8bLw+PB9fHv4z3h3YiL'
    b'f61nBfxMBa+I29OHjTuWSAWY+Jls5WdqjalKeJ8ZsMcffj8fRm3E8vtesvxsPp5ThcXgvWnTLJJbINaIF/tttbPtpHnqlub0X4BlEcsQi/qO'
    b'0QnRvOzpbfQjeRHKWHcX9+pwy/HG8PL0T8i/EwsbG6+PoRAVZxOPUlw9v6RxyTqSxCyLVt4vfauXfj/fRKE7+QZidfy/9hnDU5lSAYArMtCV'
    b'CywY/HTfBj6VsJP+TuK4arHCDR+dmQfwanl5r+mZS85sfAXIyPp/fj/fFLZfULlbGyesrvMcELwTqD99OH8TjdKwt32pEPAi45isxB5XF4Nd'
    b'5ot94+vhgfdBYeT1/5HHCAWZhfxK0peL1YvqXB8nEJorcQJVv2IYwlinkyBlCmV23bbseB6hd+XlxADyL74fhWuN8L4904TA+qtsogBL96fG'
    b'1CBN2J3J2IPIoomb1wm2lm768A+aXB+QNJmPH7Kustnrb1T50nzTGd9YDRmPzBBD8BRCxjPEm1Fl9ibC1Ov7q94cclRVFxjyLHsWOr/FmUl6'
    b'cgmgUl2TV6EsE8SAPLX3iQxK+FmFOLAk9n5fx00i7rMT3pNMs+iWz/3MufDtT0nP4puOZgPd5lxubNr8I0t2Ov+zGJ2gKInoDDTBTqfFZI+d'
    b'KHaLDbAqHOkBFQa3YwbWdLxJCHIncncnfS2PggepQwZvIcmWchyU2aNlWkd2PgDY3Jm33hnHY58fsAka/UmF6krQfpZW1SsU1IASxnUmiFkK'
    b'kGejS5EITE40zqqONwtP1YBA+KYTMsEJR21plbYrLM77VBBDzA2IhCd1uy6fOi/5TBCuCfDM0/2/HT3+3I2QBqxw0IcJRdSq+zF3IRSN0rgw'
    b'9IEYZ4ZzlSRCVP5/dfwLRu/xF0xsebMZZP/xxrhy8ZAtOg/IjMBAg2/bI5IyUsPEFSjZApfdKHucrMowA/SO4hVuTIHiVKqZJNyrQ3gExSrk'
    b'v2s8Z6HZnBYGyFz7444kv2+ihtLzpnHTgPKJuBnhCNT2/0uxxr0aPIOlsWXSAlXCaIsyViJoh9FDHKdO6LJpsHBKKqhpCkfGnXWTQOYUDXZj'
    b'cmtxujbfy6ReWzsexGyGHHj8Yfkk26M5ddJ2vKntopx85MgKckF5ImiqjdMcniUgHrbDp7JhPBBoeTUPgs9INRb2heKdEa4EnoRLctwU8J98'
    b'QIWTQABUYH2GOVKQRMhAxBrDI1+9CWLlFtjqsgG7aIzqBumKyd9QGP0I5efCGNMz6VKDak9MVEzp5IOIfm1+TVZpFeCJ+Ene0d73IkG85SEb'
    b'vj3LWoPO8l2B9KI30+ezPWxJM9bajW9u1amEJ6hcnYiVEyzCWEc4vSAcnegQqeZTWJF5pF3wb7YhHjlCUiojqHnaXOmomX3UR8VtH4JT7LzC'
    b'eZNHevA4aQAkdIR2iTkNg5nxKSqDcTTEf0WpLFnigT2Cc7u7mQbHJNyoRKQm7JlO2O6XhJj3+cmhzrB0MTaBxrmS+WqxgR4wwugXEuu8Sg2C'
    b'wUMmp7sWpP8SGT7IMAu1QFsEmiF6KUZJMqkvRLMk4ZnLi4NN9qXq+v79Bnk067j8k15hInLWU6ZzCykOuS8M4paCbJgr2o2gAQLkmAcZuSAQ'
    b'jxzMuzL9nLeVP7mGehyUoejsQznswxd+Zcb2DWFjbWhVSL/GCOLpHdWfVnUZMiYLUj3iX7i1j5FntpA0qcimjaRwE+yAlZpDPZWcWXjOumhN'
    b'i8UZoXctqokC2f7cyNDt70u13kaHeSSF5u0VlqoGz8npRB3rmeGL/EgNK3+BOTLKcN6KPaiInbt7Q7tueP6BKZ51vfoonT/WXb7U5QSR8rCw'
    b'RdqwzyJNWhdu+UAZgkJOKjHFk4ANQ+xucslG1StiMmpDY+28TM/cRrfI3tMWuZN7XWzMZEjL99bSveGfQO9G4VyXVQ17l3zL6WtAEULV+B+y'
    b'ZiAU9Mt1PSC+ES+2M7VjG2Vxt6LStcwkqC/PlVbWxfMk51Zc6ZhIyDJZTDPIkG25YUgLYDqsHgEyC3vzkjSMajiSeWuZc5A1Li9qqvNP7gRd'
    b'L2GPtTrn5MrAd54Z5oBhBtYNrxmRDx6wxUlhBn5kjZJUuO6/6yWzp+GcumhPB6TmTGBJ7SV1gl3hQIS/i13EZ3WJcsxCVPJ2dHyU71GYD9AT'
    b'v7nMkliyYyg6ZvTe76XM7jat7OcOtgzFpuFynHVJvfV12Gc3od8PVMzrvlhWJn0Wo/sfWok90ZyHxrWeKv+/Bf9dWawbKy6V+1m1hKOXx8yZ'
    b'jgVWcGtHhR61qsfGtAa3tum9iSuael5raky3s9j9u9dm3AFR5iaNu/wky7qpAz6e+D/B+303Er584yTXu1sfdavH3S09YaH5oxFvu3Ki1J6+'
    b'NGPont7TiojW8tB/XPsbO/5mKdspf5WVNiPMJrHMJa2rhWfefDbtxuPh7+n9J//cdfXj59/7l/Q9zuxtjpW+JG2m3Za+Fn0fxPq9IS2tiWlc'
    b'3rqV6/KJ9+2ZagnwrVtdjLOesPKNcfVJTN0j/63o/Hn3/7183/AUaoDtQkfzkUAAAAAElFTkSuQmCC'
)


def layout_sample_info():
    """Elements for Sample layout."""
    view_sample = [
        [
            sg.Frame(
                "Sample",
                key="-SAMPLE-INFO-FRAME-",
                layout=[
                    [
                        sg.Text('', key='-SAMPLE-INFO-NAME-', font=FONT_LRG, size=(50,)),
                        sg.Button(
                            'Play',
                            key='-PLAY-',
                            image_data=gs2,
                            image_subsample=1,
                            button_color=('black', sg.theme_background_color()),
                            border_width=0,
                            font=FONT_LRG,
                            tooltip='Play sample <spacebar>',
                        ),
                    ],
                    [
                        sg.Text('', key='-SAMPLE-INFO-PATH-', font=FONT_MED, size=(50,)),
                    ],
                ],
            )
        ],
        [layout_sample_settings()],  # -SAMPLE-SETTINGS-TABLE-
    ]
    return view_sample


def layout_sample_settings():
    """List the sample settings."""
    headings = ['xml_setting', 'xml_path']
    layout = [
        [
            sg.Table(
                values=[],
                headings=headings,
                # max_col_width=25,
                auto_size_columns=True,
                display_row_numbers=False,
                justification='left',
                num_rows=20,
                alternating_row_color='lightblue',
                key='-SAMPLE-SETTINGS-TABLE-',
                selected_row_colors='black on yellow',
                enable_events=True,
                expand_x=True,
                expand_y=True,
                enable_click_events=True,  # Comment out to not enable header and other clicks
                # tooltip='This is a table',
            )
        ],
    ]
    return layout


def to_tree(data):
    """Convert flat list of path parts to tree. ref https://stackoverflow.com/a/68288876 ."""
    d = defaultdict(list)
    try:
        # for a, *b in data:
        for x in data:
            a = x[0]
            if len(x) > 1:
                b = x[1:]
                d[a].append(b)
                # last_a = a
                # print(a, b)
            else:
                pass
                # print('wierd', x)
    except Exception as e:
        # print(last_a)
        # print(e, data)
        raise e
    return {a: [i for [i] in b] if all(len(i) == 1 for i in b) else to_tree(b) for a, b in d.items()}


def sample_tree_data(card, samples):
    """Take a samples iterable, and return sg tree."""
    sample_paths = [s.path.relative_to(card.card_root).parts for s in samples]

    print(sample_paths[0])

    try:
        sample_tree = to_tree(sample_paths)
    except Exception as e:
        # print(sample_paths)
        print(e)
        sample_tree = {}

    def add_nodes_in_dict(parent, node):
        # recurse the dict
        if isinstance(node, list):
            # print('LIST', node)
            for itm in node:
                path = parent + itm
                treedata.Insert(parent, path, itm, values=[], icon=file_icon)
        else:
            # print('DICT', node.keys())
            for key, itm in node.items():
                path = parent + key + '/'
                treedata.Insert(parent, path, key, values=[], icon=folder_icon)
                add_nodes_in_dict(path, itm)

    treedata = sg.TreeData()
    add_nodes_in_dict('', sample_tree)
    return treedata


filter_tooltip = """Filter files\nEnter a string in box to narrow down the list of files.\n
    File list will update with list of files with string in filename."""

filter_layout = [
    [
        sg.Text('Filter (F2):', font=FONT_MED, size=(15,)),
        sg.Input(size=(25, 1), enable_events=True, key='-FILTER-', tooltip=filter_tooltip, font=FONT_MED),
        sg.T(size=(15, 1), k='-FILTER NUMBER-', font=FONT_MED),
    ]
]


def layout_sample_tree():
    """A layout a samples treem attributes."""
    layout = [
        [
            sg.Tree(
                font=FONT_MED,
                data=sg.TreeData(),
                headings=[],
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
