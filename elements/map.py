
from vector import vec2
from pyglet import (text, shapes, graphics)
from typing import (TYPE_CHECKING)


if TYPE_CHECKING:
    from game import Game


class Map:
    """A top-down map showing the player's current location."""
    cols: int = 10
    rows: int = 10
    size: int = 20

    def __init__(self, game: 'Game', x: int, y: int):

        self.pos: vec2 = vec2(x, y)

        self.game = game

        self.batch = graphics.Batch()

        self.e_box = shapes.Rectangle(x, y, Map.cols * Map.size, Map.rows * Map.size, color=(50, 50, 50), batch=self.batch)

        self.e_player = shapes.Rectangle(x, y, Map.size, Map.size, color=(255, 255, 255), batch=self.batch)

    def draw(self):

        x, y = self.game.player.pos

        self.e_player.x = self.pos.x + (x * Map.size)
        self.e_player.y = self.pos.y + ((Map.rows - y) * Map.size)

        self.batch.draw()
