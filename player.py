#!/usr/bin/python3 env
import items
import random

from vector import vec2
from entity import LivingEntity
from inventory import InventoryHolder


class Player(LivingEntity, InventoryHolder):

    def __init__(self, game):

        InventoryHolder.__init__(self, game)
        LivingEntity.__init__(self, game, name='You')

        # the position of the player
        self.pos = vec2(0, 0)

        self.victory = False

        self.game = game

        self.give_item(items.Gold(game, 15), items.Rock(game))

        # slots
        self.item_slots = {}

        # strings
        # -------

        self.str_possessive = "Your"

        self.str_name = "You"

    def move(self, dx, dy):
        self.pos += (dx, dy)

        # self.game.log(world.tile_exists(self.pos).intro_text())

    def move_up(self):
        self.move(dx=0, dy=-1)

    def move_down(self):
        self.move(dx=0, dy=1)

    def move_right(self):
        self.move(dx=1, dy=0)

    def move_left(self):
        self.move(dx=-1, dy=0)

    def do_action(self, action, **kwargs):
        action_method = getattr(self, action.method.__name__)
        if action_method:
            action_method(**kwargs)

    def flee(self):
        """Moves the player randomly to an adjacent tile"""

        available_moves = self.game.get_movement_actions()
        print(f"av moves: { available_moves }")
        random_room = random.randint(0, len(available_moves) - 1)

        self.game.log('You have fled to another room')

        self.do_action(available_moves[random_room])

    def think(self):

        self.game.game_state = 'input'
