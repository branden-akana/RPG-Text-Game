#!/usr/bin/python3 env


class Enemy:

    def __init__(self, name, hp, damage):
        self.name = name
        self.hp = hp
        self.damage = damage

    def is_alive(self):
        return self.hp > 0

    def hurt(self, damage):
        self.hp -= damage

    def get_health(self):
        return self.hp


class GiantSpider(Enemy):
    def __init__(self):
        super().__init__(
            name='Giant Spider',
            hp=10,
            damage=2
        )


class Ogre(Enemy):
    def __init__(self):
        super().__init__(
            name='Ogre',
            hp=30,
            damage=15
        )
