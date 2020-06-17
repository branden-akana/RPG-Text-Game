#!/usr/bin/python3 env

from player import Player
from vector import vec2


def format_actions(actions: list) -> str:
    """Formats a list of actions as a user-readable string."""

    lines = [f'{ action.key }: { action.desc }' for action in actions]

    return '\n'.join(lines)


def format_vector(vec: vec2) -> str:
    """Formats a vector as a user-readable string."""

    lines = []

    if vec.x > 0:
        lines.append(f'up by { vec.x }')
    elif vec.x < 0:
        lines.append(f'down by { -vec.x }')

    if vec.y > 0:
        lines.append(f'right by { vec.y }')
    elif vec.y < 0:
        lines.append(f'left by { -vec.y }')

    return 'Move ' + 'and'.join(lines)


class Action():
    """An action that can be taken."""

    def __init__(self, desc: str, key: str):

        # the description of this action
        self.desc = desc or "unknown action"

        # the hotkey that will run this action
        self.key = key

    def do_action(self):
        """Run the action."""
        pass

    @staticmethod
    def register(actions: list, key: str, desc: str = 'a custom action'):
        """Decorator that creates an Action and adds it to a list."""

        def register_inner(func):

            # define a custom class that runs the wrapped fn
            class CustomAction(Action):
                def __init__(self):
                    Action.__init__(self, desc, key)

                def do_action(self):
                    func()

            # add an instance of this class to our list of actions
            actions.append(CustomAction())

            return func
        return register_inner


class PlayerAction(Action):
    """An action that is run on a player."""

    def __init__(self, player: Player, key: str, desc: str = None):

        super().__init__(desc, key)

        # the player to run this action on
        self.player: Player = player


class MoveUp(PlayerAction):

    def __init__(self, player):
        super().__init__(player, 'w', 'move up')

    def do_action(self):
        self.player.move_up()


class MoveDown(PlayerAction):

    def __init__(self, player):
        super().__init__(player, 's', 'move down')

    def do_action(self):
        self.player.move_down()


class MoveRight(PlayerAction):

    def __init__(self, player):
        super().__init__(player, 'd', 'move right')

    def do_action(self):
        self.player.move_right()


class MoveLeft(PlayerAction):

    def __init__(self, player):
        super().__init__(player, 'a', 'move left')

    def do_action(self):
        self.player.move_left()


class Attack(PlayerAction):

    def __init__(self, player: Player, enemy):
        super().__init__(player, 'k', 'Attack')
        self.enemy = enemy

    def do_action(self):
        self.player.attack(self.enemy)


class Flee(PlayerAction):

    def __init__(self, player: Player):
        super().__init__(player, 'j', 'Flee!')

    def do_action(self):
        self.player.flee()


class CheckInventory(PlayerAction):
    """Prints the player's inventory"""
    def __init__(self, player):
        super().__init__(player, 'i', 'View inventory')

    def do_action(self):

        desc = self.player.describe_inventory()
        self.player.game.add_log(desc)


class CheckBodyAction(PlayerAction):

    def __init__(self, player):
        super().__init__(player, 'c', '(debug) check body')
        self.player = player

    def do_action(self):
        lines = ['You have:']
        for part in self.player.body.parts.values():
            lines.append(f'{part.name} ({ part.status }) -> {part.attachments}')

        self.player.game.add_log('\n'.join(lines))
