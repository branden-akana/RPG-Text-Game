#!/usr/bin/python3 env

from vector import vec2
from typing import (
    TYPE_CHECKING,
    Callable
)

if TYPE_CHECKING:
    from player import Player


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

    def __init__(self, desc: str, fn=None):
        # the description of this action
        self.desc = desc or "unknown action"

        self.fn = fn or self.do_action

    def do_action(self):
        """Run the action."""
        pass

    def __call__(self):
        self.fn()


class QuickAction(Action):
    """An action that is bound to a hotkey."""

    def __init__(self, key: str, desc: str, fn=None):
        Action.__init__(self, desc, fn)

        # the hotkey that will run this action
        self.key = key

    @staticmethod
    def register(actions: list, key: str, desc: str = 'a custom action'):
        """Decorator that creates an Action and adds it to a list."""

        def register_inner(func):

            # define a custom class that runs the wrapped fn
            class CustomAction(QuickAction):
                def __init__(self):
                    QuickAction.__init__(self, key, desc)

                def do_action(self):
                    return func()

            # add an instance of this class to our list of actions
            actions.append(CustomAction())

            return func
        return register_inner


class CommandAction(Action):
    """An action that is bound to a command."""

    def __init__(self, terms: list, desc: str):
        Action.__init__(self, desc)

        # the list of command terms that will run this action
        self.terms = terms

    def do_command(self, *args):
        pass

    def do_action(self):
        return self.do_command()

    @staticmethod
    def register(actions: list, terms: list, desc: str = 'a custom action'):
        """Decorator that creates an Action and adds it to a list."""

        def register_inner(func):

            # define a custom class that runs the wrapped fn
            class CustomAction(CommandAction):
                def __init__(self):
                    CommandAction.__init__(self, terms, desc)

                def do_command(self, *args):
                    return func(*args)

            # add an instance of this class to our list of actions
            actions.append(CustomAction())

            return func
        return register_inner


def create_action(desc: str, fn: Callable, key: str = '', terms: list = []) -> Action:
    """Create a new action."""
    if key:
        # make a quick action
        class CustomAction(QuickAction):
            def __init__(self):
                super().__init__(key, desc)

            def do_action(self):
                fn()

    elif terms:
        # make a command action
        class CustomAction(CommandAction):
            def __init__(self):
                super().__init__(terms, desc)

            def do_command(self, *args):
                fn(*args)

    else:
        # make a normal action
        class CustomAction(Action):
            def __init__(self):
                super().__init__(desc)

            def do_action(self):
                fn()

    return CustomAction()


class PlayerAction(Action):
    """An action that is run on a player."""

    def __init__(self, player: 'Player', key: str, desc: str):

        super().__init__(desc)

        self.key = key

        # the player to run this action on
        self.player = player


class MoveUp(PlayerAction):

    def __init__(self, player):
        super().__init__(player, 'w', 'move up')

    def do_action(self, *args):
        self.player.move_up()


class MoveDown(PlayerAction):

    def __init__(self, player):
        super().__init__(player, 's', 'move down')

    def do_action(self, *args):
        self.player.move_down()


class MoveRight(PlayerAction):

    def __init__(self, player):
        super().__init__(player, 'd', 'move right')

    def do_action(self, *args):
        self.player.move_right()


class MoveLeft(PlayerAction):

    def __init__(self, player):
        super().__init__(player, 'a', 'move left')

    def do_action(self, *args):
        self.player.move_left()


class Attack(PlayerAction):

    def __init__(self, player: 'Player', enemy):
        super().__init__(player, 'k', 'Attack')
        self.enemy = enemy

    def do_action(self):
        self.player.attack(self.enemy)


class Flee(PlayerAction):

    def __init__(self, player: 'Player'):
        super().__init__(player, 'j', 'Flee!')

    def do_action(self):
        self.player.flee()


class CheckInventory(PlayerAction):
    """Prints the player's inventory"""
    def __init__(self, player):
        super().__init__(player, 'i', 'View inventory')

    def do_action(self):

        desc = self.player.describe_inventory()
        self.player.game.log(desc)


class CheckBodyAction(PlayerAction):

    def __init__(self, player):
        super().__init__(player, 'c', '(debug) check body')
        self.player = player

    def do_action(self):
        lines = ['You have:']
        for part in self.player.body.parts.values():
            lines.append(f'{part.name} ({ part.status }) -> {part.attachments}')

        self.player.game.log('\n'.join(lines))
