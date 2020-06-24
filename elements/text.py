
import pyglet

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from game import Game


class Text:

    def __init__(self, game: 'Game', x, y, text: str, style: str = 'normal',
                 fg=None, bg=None, alpha: float = 1.0,
                 padding=10):

        def _get_color(idx, default):
            try:
                return game.colorscheme[idx]
            except Exception:
                return default

        if not fg or type(fg) is int:
            self.fg_color = _get_color(fg, (255, 255, 255)) + (int(255 * alpha),)
        else:
            self.fg_color = fg

        if not bg or type(bg) is int:
            self.bg_color = _get_color(bg, (0, 0, 0))
        else:
            self.bg_color = bg

        self.e_label = pyglet.text.Label(
            text,
            font_name=['Courier New', 'Hack'],
            font_size=11,
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
