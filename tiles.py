#!/usr/bin/python3 env
import items
import enemies
import actions

from entity import LivingEntity
from vector import vec2, Direction


class Room:
    def __init__(self):

        self.game = None

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
    def intro_text(self):
        return """
        You find yourself in a cave with a flickering torch on the wall.
        You can make out four paths, each equally as dark and foreboding.
        """.strip()

    def modify_player(self, player):
        # Room has no action on player
        pass


class LootRoom(Room):

    def __init__(self, item):

        super().__init__()

        self.entities.append(item)
        self.item = item

    def add_loot(self, player):
        player.inventory.append(self.item)

    def modify_player(self, player):
        self.add_loot(player)


class EnemyRoom(Room):

    def __init__(self, enemy):

        super().__init__()

        self.entities.append(enemy)
        self.enemy = enemy

    def modify_player(self, the_player):

        if self.enemy.is_alive():
            # TODO: put into an Enemy.attack method
            part = the_player.hurt(self.enemy.damage)
            self.game.add_log(f'An enemy hits your { part.name } and '
                              f'does { self.enemy.damage } !')

    def get_actions(self, ent: LivingEntity):

        if self.enemy.is_alive():
            return [actions.Flee(ent), actions.Attack(ent, enemy=self.enemy)]
        else:
            return []


class EmptyCavePath(Room):
    def intro_text(self):
        return """
        Another unremarkable part of the cave. You must forge onwards.
        """.strip()

    def modify_player(self, player):
        # Room has no action on player
        pass


class GiantSpiderRoom(EnemyRoom):
    def __init__(self):
        super().__init__(enemies.GiantSpider())

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
    def __init__(self):
        super().__init__(enemies.Ogre())

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
    def __init__(self):
        super().__init__(items.Gold(10))

    def intro_text(self):
        return """
        Your torch lits a faint gold coin in the room.
        What luck!
        """.strip()


class FindDaggerRoom(LootRoom):
    def __init__(self):
        super().__init__(items.Dagger())

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
