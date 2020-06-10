#!/usr/bin/python3 env
import world
from player import Player


class Game():

    def __init__(self):

        self.player  = Player(self)  # the current Player instance

        self.actions = []  # a list of possible actions
        self.status  = ''  # a string describing the current situation

        self.next_key_press = ""  # the next key to read from the user

        self.room = None  # the current room the player is in

        self.log = []  # list of log messages

        # load the world
        world.load_tiles()

        self.player.location_x = 2
        self.player.location_y = 4

        # update the current room
        self.update_room()

        print(f'loaded a new game')

    def update_room(self):

        print(f'retrieving room @ { self.player.location_x, self.player.location_y }')

        # get the tile at the current position
        self.room = world.tile_exists(self.player.location_x, self.player.location_y)
        self.room.modify_player(self.player)

        # update the current status
        self.status = self.room.intro_text()

        # update the current actions
        self.actions = self.room.available_actions()


    def send_log_message(self, msg):

        self.log.insert(0, msg)
        if len(self.log) > 5:
            del self.log[5]


    def send_key_press(self, key):
        """Set the next key to input and update the game."""

        self.next_key_press = key
        self.update()


    def get_room(self, x, y):

        return world.tile_exists(x, y)


    def update(self):

        if self.player.is_alive() and not self.player.victory:

            # check to do any actions
            for action in self.actions:
                if self.next_key_press == action.hotkey:
                    self.player.do_action(action, **action.kwargs)
                    break

            self.update_room()

# if __name__ == '__main__':
    # play()
