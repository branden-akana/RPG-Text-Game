
import os
import subprocess


def _get_colors():

    try:  # attempt to get the current colors used by pywal.
        res = subprocess.run(['cat', os.path.expanduser('~/.cache/wal/colors')],
                             stdout=subprocess.PIPE)
        lines = res.stdout
        colors = []

        if lines:
            for line in lines.splitlines():
                # print('{} {} {}'.format(line[1:3], line[3:5], line[5:7]))
                r = int(line[1:3], 16)
                g = int(line[3:5], 16)
                b = int(line[5:7], 16)
                colors.append((r, g, b))

        return colors

    except Exception:
        return [(0, 0, 0),
                (255, 255, 255),
                (255, 255, 255),
                (255, 255, 255),
                (255, 255, 255),
                (255, 255, 255),
                (255, 255, 255),
                (255, 255, 255)
                ] * 2


class Colors:
    """A colorscheme to use for the game."""

    def __init__(self):
        # try to automatically find a colorscheme
        self.colors: list = _get_colors()

    def __getitem__(self, i):
        return self.colors[i]
