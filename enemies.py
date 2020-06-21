#!/usr/bin/python3 env

from entity import LivingEntity


class Enemy(LivingEntity):

    def __init__(self, game, name, damage):

        super().__init__(game, name)

        self.damage = damage

        #TODO: be able to set HP


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
