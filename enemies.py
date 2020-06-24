#!/usr/bin/python3 env

from entity import LivingEntity
from player import Player
from actions import create_action


class Enemy(LivingEntity):

    def __init__(self, game, name, damage):

        super().__init__(game, name)

        self.damage = damage

        #TODO: be able to set HP

    def think(self):

        # find player
        for ent in self.game.get_entities():
            if type(ent) is Player:

                def _attack():
                    # self.game.log(f'{self.name} is attacking {ent.name}!', fg=1)
                    self.attack(ent)

                return create_action('', _attack)

        return super().think()


class GiantSpider(Enemy):
    def __init__(self, game):
        super().__init__(game,
            name='Giant Spider',
            # hp=10,
            damage=2
        )


class Ogre(Enemy):
    def __init__(self, game):
        super().__init__(game,
            name='Ogre',
            # hp=30,
            damage=15
        )
