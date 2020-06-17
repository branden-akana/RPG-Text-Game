#!/usr/bin/python3 env

import world
import actions

from tiles import Room
from dataclasses import dataclass
from vector import vec2
from player import Player


@dataclass
class Message():
    text: str
    style: str = 'normal'
    fg: int = 0
    bg: int = 0


class Game():

    def __init__(self):

        # a string describing the current situation
        self.status = ''

        # the next key to read from the user
        self.next_key_press = ""

        # the current room the player is in
        self.room = None

        # list of log messages
        self.log = []

        # load the world
        self.world = world.parse_world(self)

        # the current Player instance
        self.player: Player = Player(self)

        self.player.pos = vec2(2, 4)

        # update the current room
        self.update_room()

        print('loaded a new game')

    def update_room(self):

        self.add_log(f'retrieving room @ { self.player.pos }', 8)

        # get the tile at the current position
        self.room = self.world.get_room_at(self.player.pos)

        if self.room:
            self.room.modify_player(self.player)

        # TODO: Room.intro_text() is deprecated

    def add_log(self, msg, fg=15, bg=0, style='normal'):

        # insert to the front of the list
        self.log.insert(0, Message(msg, style, fg, bg))
        if len(self.log) > 10:
            del self.log[10]

    def send_key_press(self, key):
        """Set the next key to input and update the game."""

        self.next_key_press = key
        self.update()

    def get_room(self, x, y) -> str:
        """Get a room by its coordinates."""

        return self.world.get_room_at(vec2(x, y))

    def update(self):

        if self.player.is_alive() and not self.player.victory:

            # check to do any actions
            for action in self.get_actions():
                if self.next_key_press == action.key:
                    action.do_action()
                    break

            self.update_room()

    def get_movement_actions(self) -> list:
        """Get all movement actions that the player can do."""
        return self.world.get_movement_actions(self.player.pos, self.player)

    def get_actions(self) -> list:
        """Get all actions that the player can do."""
        # self.add_log("getting actions...")

        action_list = []

        # get movement actions
        action_list += self.get_movement_actions()  # get movement actions

        # get room actions
        if self.room:
            action_list += self.room.get_actions(self.player)  # get room actions

        # debug actions
        action_list.append(actions.CheckBodyAction(self.player))
        action_list.append(actions.CheckInventory(self.player))

        return action_list

    def get_description(self, skill_check: int = 10):
        """Get a description of the room based on what the player sees.
        If a skill check is provided, change the description based
        on the value of the skill check.
        """

        if not self.room:
            return "You are out of bounds."

        lines = []

        if skill_check <= 0:  # failed check
            lines += ["You cannot see anything."]

        else:
            if self.room.light_level == 0:
                lines += ["It is too dark to see anything."]

            else:
                # get number of paths
                num_paths = len(self.get_movement_actions())
                lines += [f"There are {num_paths} paths."]

                # get entities in room
                for ent in self.room.entities:
                    lines += [f"You see a {ent.name}."]

        return ' '.join(lines)


# if __name__ == '__main__':
    # play()
