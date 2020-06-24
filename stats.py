
import random
from dataclasses import dataclass


@dataclass
class StatCheck:

    # the ability that was checked
    ability: str

    # the minimum stat to "pass" this check
    difficulty: int

    # the base stat of the creature
    base: int

    # a list of rolls to add onto this base stat
    rolls: list

    def get_total(self):
        return (self.base + sum(self.rolls))

    def is_passed(self):
        return self.get_total() >= self.difficulty

    def get_percent(self):
        return self.get_total() / self.difficulty

    def __str__(self):
        eq = str(self.base)
        for roll in self.rolls:
            eq += f'+{roll}'

        if self.is_passed():
            return f'({self.ability}?{self.difficulty} => {eq} success)'
        else:
            return f'({self.ability}?{self.difficulty} => {eq} failure)'

    def __bool__(self):
        return self.is_passed()


class AbilityStats:

    def __init__(self):

        self.ability_stats = {}

        points = 20
        abilities = ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHR']

        for ability in abilities:
            self.ability_stats[ability] = 0

        for _ in range(points):
            self.ability_stats[random.choice(abilities)] += 1

    def get_base_ability_score(self, ability):
        """Get the score for an ability."""
        return self.ability_stats[ability]

    def ability_roll(self, ability, num_dice=2):

        rolls = []
        for _ in range(num_dice):  # number of rolls
            rolls.append(random.randint(1, 6))

        return [self.get_base_ability_score(ability)] + rolls

    def ability_check(self, difficulty, ability):

        rolls = []
        for _ in range(2):  # number of rolls
            rolls.append(random.randint(1, 6))

        return StatCheck(
            ability,
            difficulty,
            self.get_base_ability_score(ability),
            rolls
        )
