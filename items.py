#!/usr/bin/python3 env

from entity import Entity


class Item(Entity):
    """The base class for all items"""
    def __init__(self, game, name, description, value, amount=1):

        Entity.__init__(self, game, name)

        # a description of the item
        self.description = description

        # the price of this item (per item)
        self.value = value

        # the amount of this item (stacking)
        self.amount = amount

    def __str__(self):
        return "{}\n=====\n{}\nValue: {}\n".format(
                self.name, self.description, self.amount
            )


class Gold(Item):
    def __init__(self, game, value):
        super().__init__(
            game,
            name="Gold",
            description="A round coin with {} stamped on the front.".format(
                    str(value)
                ),
            value=value,
        )


class Weapon(Item):
    def __init__(self, game, name, description, value, damage):

        super().__init__(game, name, description, value)

        # the base damage of the weapon
        self.damage = damage

    def __str__(self):
        return "{}\n=====\n{}\nValue: {}\nDamage: {}".format(
                self.name, self.description, self.value, self.damage
        )


class Rock(Weapon):
    def __init__(self, game):
        super().__init__(
            game,
            name="Rock",
            description="A fist-sized rock, suitable for bludgeoning.",
            value=0,
            damage=5
        )


class Dagger(Weapon):
    def __init__(self, game):
        super().__init__(
            game,
            name="Dagger",
            description="A small dagger with some rust."
                        "Somewhat more dangerous than a rock.",
            value=10,
            damage=10
        )
