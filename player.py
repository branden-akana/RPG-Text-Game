#!/usr/bin/python3 env
import items
import world
import random


class Player():
    def __init__(self):
        self.inventory = [items.Gold(15), items.Rock()]
        self.hp = 100
        self.location_x, self.location_y = world.starting_position
        self.victory = False

    def is_alive(self):
        return self.hp > 0

    def print_inventory(self):
        for item in self.inventory:
            print(item, '\n')

    def move(self, dx, dy):
        self.location_x += dx
        self.location_y += dy
        print(world.tile_exists(self.location_x, self.location_y).intro_text())

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

        print('You use {} against {}!'.format(best_weapon.name, enemy.name))
        enemy.hp -= best_weapon.damage
        if not enemy.is_alive():
            print('You killed a {}!'.format(enemy.name))
        else:
            print('{} HP is {}.'.format(enemy.name, enemy.hp))

    def do_action(self, action, **kwargs):
        action_method = getattr(self, action.method.__name__)
        if action_method:
            action_method(**kwargs)

    def flee(self, tile):
        """Moves the player randomly to an adjacent tile"""
        available_moves = tile.adjacent_moves()
        print(f"av moves: { available_moves }")
        random_room = random.randint(0, len(available_moves) - 1)
        self.do_action(available_moves[random_room])
