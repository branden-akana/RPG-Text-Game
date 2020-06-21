#!/usr/bin/python3 env
import typing
import items
import enemies
import actions

from entity import LivingEntity
from vector import vec2, Direction


if typing.TYPE_CHECKING:
    from player import Player
    from game import Game


class Room:
    def __init__(self, game: 'Game'):

        self.game: 'Game' = game

        # a list of entities in this room
        self.entities = []

        # a description of this room
        self.desc = "a room"

        # the level of brightness in the room
        # 0 => pitch black
        # 50 => normal
        # 100 => blinding
        self.light_level = 50

        # the temperature level in the room
        # 0 => freezing
        # 50 => normal
        # 100 => extremely hot
        self.temp_level = 50

    def intro_text(self):
        raise NotImplementedError()

    def modify_player(self, player):
        raise NotImplementedError()

    def get_actions(self, ent: LivingEntity) -> list:
        """Returns all of the available actions in this room."""

        return []


class StartingRoom(Room):

    def __init__(self, game: 'Game'):
        Room.__init__(self, game)

    def intro_text(self):
        return """
        You find yourself in a cave with a flickering torch on the wall.
        You can make out four paths, each equally as dark and foreboding.
        """.strip()

    def modify_player(self, player):
        # Room has no action on player
        pass


class LootRoom(Room):

    def __init__(self, game: 'Game', item):

        Room.__init__(self, game)

        self.entities.append(item)

    def add_loot(self, player: 'Player'):
        for item in [ent for ent in self.entities if isinstance(ent, items.Item)]:
            player.give_item(item)
            self.entities.remove(item)

    def modify_player(self, player):
        self.add_loot(player)


class EnemyRoom(Room):

    def __init__(self, game: 'Game', enemy):

        Room.__init__(self, game)

        self.entities.append(enemy)
        self.enemy = enemy

    def modify_player(self, the_player):

        if self.enemy.is_alive():
            # TODO: put into an Enemy.attack method
            part = the_player.hurt(self.enemy.damage)
            self.game.log(f'An enemy hits your { part.name } and '
                              f'does { self.enemy.damage } !')

    def get_actions(self, ent: LivingEntity):

        if self.enemy.is_alive():
            # return [actions.Flee(ent), actions.Attack(ent, enemy=self.enemy)]
            return [actions.Flee(ent)]
        else:
            return []


class EmptyCavePath(Room):

    def __init__(self, game: 'Game'):
        Room.__init__(self, game)

    def intro_text(self):
        return """
        Another unremarkable part of the cave. You must forge onwards.
        """.strip()

    def modify_player(self, player):
        # Room has no action on player
        pass


class GiantSpiderRoom(EnemyRoom):

    def __init__(self, game: 'Game'):
        EnemyRoom.__init__(self, game, enemies.GiantSpider(game))

    def intro_text(self):
        if self.enemy.is_alive():
            return """
            A giant spider jumps down from its web in front of you!
            """.strip()
        else:
            return """
            The corpse of a dead spider rots on the ground.
            """.strip()


class OgreRoom(EnemyRoom):
    def __init__(self, game):
        super().__init__(game, enemies.Ogre(game))

    def intro_text(self):
        if self.enemy.is_alive():
            return """
            An Ogre appears from the shadows!
            """.strip()
        else:
            return """
            The corpse of a dead ogre rots on the ground.
            """.strip()


class FindGoldRoom(LootRoom):
    def __init__(self, game):
        super().__init__(game, items.Gold(game, 10))

    def intro_text(self):
        return """
        Your torch lits a faint gold coin in the room.
        What luck!
        """.strip()


class FindDaggerRoom(LootRoom):
    def __init__(self, game):
        super().__init__(game, items.Dagger(game))

    def intro_text(self):
        return """
        Your notice something shiny in the corner.
        It's a dagger! You pick it up.
        """.strip()


class LeaveCaveRoom(Room):
    def intro_text(self):
        return """
        You see a bright light in the distance...
        ... it grows as you get closer! It's sunlight!

        Victory is yours!
        """.strip()

    def modify_player(self, player):
        player.victory = True
