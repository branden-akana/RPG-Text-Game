#!/usr/bin/python3 env

import world
import actions

from tiles import Room
from dataclasses import dataclass
from vector import vec2
from player import Player

QuickAction = actions.QuickAction
CommandAction = actions.CommandAction


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

        # the state of the action menu
        # tells the game what actions to display
        self.menu_state = 'main'

        # holds an item previously selected through the menu
        self.menu_selected_item = None

        # holds the command string that is being typed by the user
        self.menu_cmd_buffer = ''

        # if true, try to quit the game
        self.quit = False

        # update the current room
        self.set_current_room()

        print('loaded a new game')

    def set_current_room(self):

        # self.add_log(f'retrieving room @ { self.player.pos }', 8)
        # get the tile at the current position
        self.room = self.world.get_room_at(self.player.pos)

        # TODO: Room.intro_text() is deprecated

    def do_tick(self):
        """Calculate one unit of time."""

        if self.room:
            self.room.modify_player(self.player)

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

        if self.menu_state == 'cmd':
            key = self.next_key_press
            # add the last pressed key to the cmd buffer
            if key == 'KEY_BACKSPACE':
                # remove last character
                self.menu_cmd_buffer = self.menu_cmd_buffer[:-1]
            elif key == '\n':
                # TODO: run a command
                self.add_log('running command: ' + self.menu_cmd_buffer)
                self.run_command(self.menu_cmd_buffer)
                self.menu_cmd_buffer = ''
                self.menu_state = 'main'
            else:
                self.menu_cmd_buffer += self.next_key_press

        elif self.next_key_press == ':':
            # set the menu to cmd mode
            self.menu_state = 'cmd'

        elif self.player.is_alive() and not self.player.victory:
            # check to do any actions
            for action in self.get_actions():
                if self.next_key_press == action.key:
                    action.do_action()
                    self.do_tick()
                    self.set_current_room()
                    break

    def get_commands(self) -> list:
        """Get all commands that the player can do."""

        commands = []

        @CommandAction.register(commands, ['help'], 'get a list of commands')
        def _cmd_help(*args):
            self.add_log('There is no help.')

        @CommandAction.register(commands, ['quit'], 'quit the game')
        def _cmd_quit(*args):
            self.quit = True

        return commands

    def run_command(self, cmd: str):

        args = cmd.split(' ')
        root = args[0]
        args = args[1:]

        for command in self.get_commands():
            if root in command.terms:
                command.do_command(args)

    def get_movement_actions(self) -> list:
        """Get all movement actions that the player can do."""
        return self.world.get_movement_actions(self.player.pos, self.player)

    def get_actions(self) -> list:
        """Get all actions that the player can do."""
        # self.add_log("getting actions...")

        action_list = []

        if self.menu_state == 'main':

            # get movement actions
            action_list += self.get_movement_actions()  # get movement actions

            # get room actions
            if self.room:
                action_list += self.room.get_actions(self.player)  # get room actions

            # debug actions
            action_list.append(actions.CheckBodyAction(self.player))
            action_list.append(actions.CheckInventory(self.player))

            @QuickAction.register(action_list, 'e', 'equip an item')
            def _equip():
                self.menu_state = 'equip_item'

        elif self.menu_state == 'equip_item':

            for i, item in enumerate(list(self.player.inventory.keys())):

                @QuickAction.register(action_list, str(i+1), f'select {item.name}')
                def _select_item(item=item):
                    self.menu_selected_item = item
                    self.menu_state = 'equip_part'

        elif self.menu_state == 'equip_part':

            for i, part in enumerate(self.player.body.get_equippable_parts()):

                @QuickAction.register(action_list, str(i+1), f'select {part.name}')
                def _action(part=part):
                    item = self.menu_selected_item
                    self.add_log(f'your {part.name} is now holding {item.name}')
                    self.menu_selected_item = None
                    self.menu_state = 'main'

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
