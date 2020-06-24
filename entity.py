
import typing
import body
import random
from stats import AbilityStats
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

    def get_name(self) -> str:
        return self.name

    def __eq__(self, o):

        if type(self) == type(o):
            return self.name == o.name
        else:
            return self == o

    def __hash__(self):
        return hash(self.name)


class LivingEntity(Entity, AbilityStats):
    """Represents an entity that has a body and is able to die."""

    def __init__(self, game: 'Game', name: str):

        Entity.__init__(self, game, name)
        AbilityStats.__init__(self)

        # the body of the entity
        self.body = body.HumanoidBody(game, self)

    def hurt(self, damage):
        return self.body.hurt(damage)

    def get_health(self) -> int:
        return self.body.health

    def get_name(self) -> str:
        if self.is_alive():
            return self.name
        else:
            return 'corpse of a ' + self.name

    def is_alive(self) -> int:
        return self.body.is_alive()

    def attack(self, ent: Entity):
        """Attack an entity."""

        # attacker checks
        dmg_check = self.ability_check(10, 'STR')
        hit_check = self.ability_roll('DEX', 3)

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
        # for now automatically find the best weapon
        part = parts[0]
        for _part in parts:
            if _part.get_base_damage() > part.get_base_damage():
                part = _part

        # calculate damage to deal

        dmg = 1

        if part.can_attack_armed and part.held_item:
            # self.game.log(
                # f'{self.name} attacks {ent.get_name()} with {part.name} holding {part.held_item.name}!'
            # )
            dmg = part.held_item.damage
            weapon = part.held_item
        elif part.can_attack_bare:
            # self.game.log(
                # f'{self.name} attacks {ent.get_name()} with the {part.name}!'
            # )
            weapon = part
            # TODO: implement unarmed damage stat

        # calculate effect of damage

        if isinstance(ent, LivingEntity):
            # defender checks
            dodge_check = ent.ability_check(sum(hit_check), 'DEX')

            if dodge_check:
                # self.game.log(f'The attack misses!')
                self.game.log(f'{self.name} misses an attack on {ent.get_name()}!')
            else:
                self.game.log(f'{self.name} hits {ent.get_name()} with a {weapon.name}!')
                def_check = ent.ability_check(10, 'CON')

                dmg = int(dmg * dmg_check.get_percent()) + 1
                hurt_part = ent.hurt(dmg)
                self.game.info(f'{ent.get_name()} takes {dmg} damage to the {hurt_part.name}!')
                if not ent.is_alive():
                    self.game.info(f'{ent.get_name()} has died')

        else:
            self.game.log('It does nothing!')

    def think(self) -> 'Action':
        """Decide an action to take for this entity's turn."""

        def _do_nothing():
            self.game.log(f'{self.name} is doing nothing.')

        return create_action('do nothing', _do_nothing)
