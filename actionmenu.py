"""
Action Menu
-----------

An action menu holds a list of actions (a key binding and a function),
a dictionary of arbitrary arguments to pass between menus,
and a menu queue (a list defining what the next menu(s) should be).

* * *

The next_menu() method pops the next menu off the queue and returns it.
If the menu queue is empty, next_menu() will return 'self', causing the next
menu to be itself.

* * *

The handle_input(cmd) method should be called whenever the Player either
presses a key (then 'cmd' will be the character corresponding to that key), or
types a command (activated by clicking ':' and typing a command, then 'cmd'
will be the entered command)

If 'cmd' matches any of the bindings in the menu's list of actions, then the
corresponding action should be called.

If an action was called, return next_menu(), otherwise return 'self'.

* * *

The ActionMenu class should be subclassed to create different menus.
In the __init__() method of the subclass, use the @self.add_option
decorator to add the decorated function as an action to the menu.

If the action needs to pass an argument to the next menu, set a key in the
'self.args' dictionary. 'self.args' will be passed to the next menu.
"""

from actions import QuickAction


class ActionMenu:
    """A handler for the action menu."""

    def __init__(self, game, **kwargs):

        # a reference to the game
        self.game = game

        # a list of actions in this menu
        self.action_list = []

        # an optional dict of arguments to pass state between menus
        self.args: dict = kwargs or {}

    def handle_input(self, cmd: str) -> 'ActionMenu':
        """Handle an input from the player (a key or a command).
        Return the menu to display after handling the input. """

        for action in self.action_list:
            if cmd == action.key:
                action()
                return self.next_menu()

        # no key matches; don't change the menu
        return self

    def next_menu(self) -> 'ActionMenu':
        """Pops the next menu in the stack and return it.

        If the popped menu is the last menu in the stack, additionally
        run the function inside args['end_fn'].
        """

        if 'menu_stack' in self.args:

            # pop the next menu from the queue
            menu_cls = self.args['menu_stack'].pop(0)

            # print(f'going to menu: {menu_cls.__name__} {[menu.__name__ for menu in self.args["menu_stack"]]}')
            # print(self.args)

            # if the queue is empty, run the end function
            if len(self.args['menu_stack']) == 0:
                self.args['end_fn'](self.args)
                # if the end function changed the player's location,
                # update the room
                self.game.set_current_room()
                # then continue the game
                self.game.game_state = 'running'

            return menu_cls(self.game, **self.args)

        return self

    def add_option(self, key: str, desc: str = 'a custom action', menu_stack=None):
        """Decorator that creates a QuickAction and adds it to this menu."""

        if menu_stack:
            main = True
        else:
            main = False
            menu_stack = self.args['menu_stack']

        def register_inner(func):

            def do_action():
                self.args['menu_stack'] = menu_stack
                if main:
                    # set the wrapped function to run at the end;
                    # then goto the next menu
                    self.args['end_fn'] = func
                else:
                    # run the wrapped function;
                    # then goto the next menu
                    func()

            # add an instance of this class to our list of actions
            self.action_list.append(QuickAction(key, desc, do_action))

            return func

        return register_inner


class InventoryMenu(ActionMenu):
    """A menu that lists all items in the player's inventory."""

    def __init__(self, game, **kwargs):
        super().__init__(game, **kwargs)

        for i, item in enumerate(list(self.game.player.inventory.keys())):

            @self.add_option(str(i+1), f'select {item.name}')
            def _select_item(self=self, item=item):
                # self.game.log(f'chose {item.name}')
                self.args['item'] = item


class BodyPartMenu(ActionMenu):
    """A menu that lists all the player's body parts that can hold an item."""

    def __init__(self, game, **kwargs):
        super().__init__(game, **kwargs)

        for i, part in enumerate(self.game.player.body.get_equippable_parts()):

            @self.add_option(str(i+1), f'select {part.name}')
            def _select_part(self=self, part=part):
                # self.game.log(f'chose {part.name}')
                self.args['part'] = part


class EntityMenu(ActionMenu):

    def __init__(self, game, **kwargs):
        super().__init__(game, **kwargs)

        # add 'yourself' as an option
        @self.add_option('1', 'yourself')
        def _self_attack():
            self.args['ent'] = self.game.player

        for i, ent in enumerate(self.game.room.entities):

            @self.add_option(str(i+2), f'{ent.get_name()}')
            def _attack(ent=ent):
                self.args['ent'] = ent


class MainMenu(ActionMenu):

    def __init__(self, game, **kwargs):
        super().__init__(game, **kwargs)

        # movement action
        for action in self.game.get_movement_actions():
            self.add_option(action.key, action.desc, [MainMenu])(action.do_action)

        # TODO: look action
        # TODO: examine action
        @self.add_option('x', 'Examine...', [EntityMenu, MainMenu])
        def _examine(args):
            ent = args['ent']
            check = self.game.player.ability_check(10, 'INT')
            if check:
                self.game.log(f'You examine the {ent.get_name()}. {check}')
                self.game.log(f'The abilities of {ent.get_name()} are:')
                for ability, score in ent.ability_stats.items():
                    self.game.log(f'{ability}: {score} ({score+2} - {score+12})')
            else:
                self.game.log(f'You fail to examine the {ent.get_name()}. {check}')

        @self.add_option('e', 'Equip an item...', [InventoryMenu, BodyPartMenu, MainMenu])
        def _equip(args):
            item, part = args['item'], args['part']
            part.held_item = item
            self.game.log(f'your {part.name} is now holding {item.name}')

        @self.add_option('t', 'Take...', [EntityMenu, MainMenu])
        def _take(args):
            ent = args['ent']
            self.game.player.give_item(ent)
            # self.game.log(f'You take the {ent.get_name()}')

        @self.add_option('k', 'Attack...', [EntityMenu, MainMenu])
        def _attack(args):
            self.game.player.attack(args['ent'])

        @self.add_option('l', 'Look around', [MainMenu])
        def _look(args):
            """Get a description of the room based on what the player sees.
            If a skill check is provided, change the description based
            on the value of the skill check.
            """
            room = self.game.room

            if not room:
                return "You are out of bounds."

            lines = []

            check = self.game.player.ability_check(2, 'WIS')

            self.game.info(f'You look around the room... {check}')

            if not check:  # failed check
                lines += ["You cannot see anything."]

            else:
                if room.light_level == 0:
                    lines += ["It is too dark to see anything."]

                else:
                    # get number of paths
                    num_paths = len(self.game.get_movement_actions())
                    lines += [f"There are {num_paths} paths."]

                    # get entities in room
                    for ent in room.entities:
                        lines += [f"You see a {ent.get_name()}."]

            self.game.log(' '.join(lines))

