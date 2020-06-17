#!/usr/bin/python3 env
import items
import random
import body

from vector import vec2


class Player():

    def __init__(self, game):

        # the position of the player
        self.pos = vec2(0, 0)

        # the body of the player
        self.body = body.HumanoidBody(game, self)

        self.victory = False

        self.game = game

        self.inventory = [items.Gold(15), items.Rock()]

        # slots
        self.item_slots = {}

        # strings
        # -------

        self.str_possessive = "Your"

        self.str_name = "You"

    def hurt(self, damage):
        return self.body.hurt(damage)

    def get_health(self) -> int:
        return self.body.health

    def is_alive(self) -> int:
        return self.body.is_alive

    def print_inventory(self):
        line = '\n'.join([str(item) for item in self.inventory])
        self.game.add_log(line)

    def move(self, dx, dy):

        self.pos += (dx, dy)

        # self.game.add_log(world.tile_exists(self.pos).intro_text())

    def move_up(self):
        self.move(dx=0, dy=-1)

    def move_down(self):
        self.move(dx=0, dy=1)

    def move_right(self):
        self.move(dx=1, dy=0)

    def move_left(self):
        self.move(dx=-1, dy=0)

    def attack(self, enemy):
        best_weapon = None
        max_damage = 0
        for item in self.inventory:
            if isinstance(item, items.Weapon):
                if item.damage > max_damage:
                    max_damage = item.damage
                    best_weapon = item

        self.game.add_log('You use {} against {}!'.format(best_weapon.name, enemy.name))
        enemy.hp -= best_weapon.damage
        if not enemy.is_alive():
            self.game.add_log('You killed a {}!'.format(enemy.name))
        else:
            self.game.add_log('{} HP is {}.'.format(enemy.name, enemy.hp))

    def do_action(self, action, **kwargs):
        action_method = getattr(self, action.method.__name__)
        if action_method:
            action_method(**kwargs)

    def flee(self):
        """Moves the player randomly to an adjacent tile"""

        available_moves = self.game.get_movement_actions()
        print(f"av moves: { available_moves }")
        random_room = random.randint(0, len(available_moves) - 1)

        self.game.add_log('You have fled to another room')

        self.do_action(available_moves[random_room])
