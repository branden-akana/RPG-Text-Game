
from vector import vec2
from pyglet import (text, shapes, graphics)
from typing import (TYPE_CHECKING)


if TYPE_CHECKING:
    from game import Game


class Map:
    """A top-down map showing the player's current location."""

    def __init__(self, game: 'Game', x: int, y: int)

        self.pos: vec2 = vec2(x, y)

        self.game = game

        self.batch = graphics.Batch()

        self.e_box = shapes.Rectangle(x, y, 100, 100, color=(50, 50, 50), batch=self.batch)

        self.e_player = shapes.Rectangle(x, y, 10, 10, color(255, 255, 255), batch=self.batch)

    def draw(self):
        self.batch.draw()
