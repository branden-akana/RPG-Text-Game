
import os
import subprocess
import pyglet

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from game import Game


def get_colors():

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


_colors: list = get_colors()


class Text:

    def __init__(self, game: 'Game', x, y, text: str, style: str = 'normal',
                 fg=None, bg=None,
                 padding=10):

        def _get_color(idx, default):
            try:
                return _colors[idx]
            except Exception:
                return default

        self.fg_color = _get_color(fg, (255, 255, 255)) + (255,)
        self.bg_color = _get_color(bg, (0, 0, 0))

        self.e_label = pyglet.text.Label(
            text,
            font_name=['Courier New', 'Hack'],
            font_size=12,
            x=x, y=y,
            width=800,
            multiline=True,
            anchor_y='bottom',
            color=self.fg_color,
        )

        self.e_background = pyglet.shapes.Rectangle(
            x - padding/2, y - padding/2,
            self.e_label.content_width + padding,
            self.e_label.content_height + padding,
            color=self.bg_color
        )

    def draw(self):
        self.e_background.draw()
        self.e_label.draw()


if __name__ == '__main__':
    # test get_colors()
    get_colors()
