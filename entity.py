
import typing
import body
import random
from actions import Action, create_action


if typing.TYPE_CHECKING:
    from game import Game


class Entity:
    """Represents an entity."""

    def __init__(self, game: 'Game', name: str):

        # a reference to the game
        self.game: 'Game' = game

        # the name of the entity
        self.name = name

    def __eq__(self, o):

        if type(self) == type(o):
            return self.name == o.name
        else:
            return self == o

    def __hash__(self):
        return hash(self.name)


class LivingEntity(Entity):
    """Represents an entity that has a body and is able to die."""

    def __init__(self, game: 'Game', name: str):

        Entity.__init__(self, game, name)

        # the body of the entity
        self.body = body.HumanoidBody(game, self)

    def hurt(self, damage):
        return self.body.hurt(damage)

    def get_health(self) -> int:
        return self.body.health

    def is_alive(self) -> int:
        return self.body.is_alive()

    def attack(self, ent: Entity):
        """Attack an entity."""

        # get body parts that can attack
        parts = [part for part in list(self.body.parts.values())
                 if part.can_attack_bare or
                 (part.can_attack_armed and part.held_item)]

        if len(parts) == 0:
            self.game.log(
                f'{self.name} tries to attack, but has nothing to attack with!'
            )
            return

        # TODO: be able to choose a specific way to attack
        # for now pick one at random
        part = random.choice(parts)

        # calculate damage to deal

        dmg = 1
        if part.can_attack_armed and part.held_item:
            self.game.log(
                f'{self.name} attacks {ent.name} with {part.name} holding {part.held_item.name}!'
            )
            dmg = part.held_item.damage
        elif part.can_attack_bare:
            self.game.log(
                f'{self.name} attacks {ent.name} with the {part.name}!'
            )
            # TODO: implement unarmed damage stat

        # calculate effect of damage

        if isinstance(ent, LivingEntity):
            hurt_part = ent.hurt(dmg)
            self.game.log(f'{self.name} does {dmg} damage to the {hurt_part.name}!')
        else:
            self.game.log('It does nothing!')

    def think(self) -> 'Action':
        """Decide an action to take for this entity's turn."""

        def _do_nothing():
            self.game.log(f'{self.name} is doing nothing.')

        return create_action('do nothing', _do_nothing)
