#!/usr/bin/python3 env

from vector import vec2, Direction
import tiles
import actions


class World:

    def __init__(self, game):

        self.game = game

        # a dict of rooms with their position as the key
        self.room_map = {}

    def set_room_at(self, pos: vec2, room: tiles.Room):
        """Add a room to the map. Will overwrite a room if it exists in the same
        location."""

        self.room_map[pos] = room

        room.game = self.game

    def get_room_at(self, pos: vec2):
        """Get a room from the map. Returns None if there is no room at that
        location."""

        return self.room_map.get(pos, None)

    def get_movement_actions(self, pos: vec2, player) -> list:
        """Returns all move actions for adjacent tiles."""

        mapping = {
            Direction.UP: actions.MoveUp,
            Direction.LEFT: actions.MoveLeft,
            Direction.RIGHT: actions.MoveRight,
            Direction.DOWN: actions.MoveDown
        }

        move_actions = []

        for direction, action in mapping.items():
            if self.get_room_at(pos + direction):
                move_actions.append(action(player))

        return move_actions


room_mapping = {
        '.': tiles.EmptyCavePath,
        '0': tiles.StartingRoom,
        '1': tiles.FindGoldRoom,
        '2': tiles.FindDaggerRoom,
        '3': tiles.GiantSpiderRoom,
        '4': tiles.OgreRoom,
        '5': tiles.LeaveCaveRoom,
}


def parse_world(game, filename='resources/map.txt') -> World:
    """Parse a world file."""

    world = World(game)

    x, y = 0, 0  # the current world location we are reading at

    print('loading world...')

    with open(filename, 'r') as file:
        for c in file.read():

            if c == '\n':
                x = 0   # reset x back to 0
                y += 1  # increment y
                continue

            # try to find the room type in our mapping
            room_type = room_mapping.get(c, None)

            if room_type:
                print(f'\tsetting loc {x, y} to {room_type.__name__}')
                world.set_room_at(vec2(x, y), room_type())

            x += 1

    print('world loaded.')
    return world


# old parser
# ------------------------------------------------------------------------------

_world = {}
starting_position = vec2(2, 4)


def load_tiles():
    """Parses a file that describes the world space into the _world object"""
    with open('resources/map.txt', 'r') as f:
        rows = f.readlines()
    x_max = len(rows[0].split('\t'))
    for y in range(len(rows)):
        cols = rows[y].split('\t')
        for x in range(x_max):
            tile_name = cols[x].replace('\n', '')
            if tile_name == 'StartingRoom':
                global starting_position
                starting_position = (x, y)
            _world[(x, y)] = None if tile_name == '' else getattr(
                __import__('tiles'), tile_name
                )(x, y)

    for x, y in _world:
        print(f"{ x }, { y }: { _world[(x, y)] }")


def tile_exists(pos: vec2):
    return _world.get((pos.x, pos.y))


if __name__ == '__main__':
    parse_world()
