#!/usr/bin/python3 env
from player import Player


class Action():
    def __init__(self, method, name, hotkey, **kwargs):
        self.method = method
        self.hotkey = hotkey
        self.name = name
        self.kwargs = kwargs

    def __str__(self):
        return '{}: {}'.format(self.hotkey, self.name)


class MoveUp(Action):
    def __init__(self):
        super().__init__(
            method=Player.move_up,
            name='Move up',
            hotkey='w'
        )


class MoveDown(Action):
    def __init__(self):
        super().__init__(
            method=Player.move_down,
            name='Move down',
            hotkey='s'
        )


class MoveRight(Action):
    def __init__(self):
        super().__init__(
            method=Player.move_right,
            name='Move right',
            hotkey='d'
        )


class MoveLeft(Action):
    def __init__(self):
        super().__init__(
            method=Player.move_left,
            name='Move left',
            hotkey='a'
        )


class ViewInventory(Action):
    """Prints the player's inventory"""
    def __init__(self):
        super().__init__(
            method=Player.print_inventory,
            name='View inventory',
            hotkey='i'
        )


class Attack(Action):
    def __init__(self, enemy):
        super().__init__(
            method=Player.attack,
            name='Attack',
            hotkey='k',
            enemy=enemy
        )


class Flee(Action):
    def __init__(self, tile):
        super().__init__(
            method=Player.flee,
            name='Flee!',
            hotkey='j',
            tile=tile
        )
