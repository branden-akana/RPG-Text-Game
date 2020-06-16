
import math

from dataclasses import dataclass


@dataclass
class vec2():
    """A 2D vector."""

    x: float
    y: float


    def distance(self, vec):
        """Get the distance from this vector to another."""

        return math.sqrt( (self.x + vec.x)**2 + (self.y + vec.y)**2 )


    def __add__(self, o):

        if type(o) is tuple and len(o) >= 2:
            # try to add the first and second elts to our x and y
            return vec2(self.x + o[0], self.y + o[1])

        elif type(o) is vec2:
            return vec2(self.x + o.x, self.y + o.y)

        else:
            raise TypeError('Cannot add vec2 and ' + type(o).__name__)

    def __eq__(self, o):

        if type(o) is tuple and len(o) >= 2:
            # try to add the first and second elts to our x and y
            return self.x == o[0] and self.y == o[1]

        elif type(o) is vec2:
            return self.x == o.x and self.y == o.y

        else:
            return self == o


    def __iter__(self):

        yield self.x
        yield self.y


    def __hash__(self):

        return hash((self.x, self.y))

class Direction:

    UP: vec2 = vec2(0, -1)
    DOWN: vec2 = vec2(0, 1)
    LEFT: vec2 = vec2(-1, 0)
    RIGHT: vec2= vec2(1, 0)

