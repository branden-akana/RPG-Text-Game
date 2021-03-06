
import random

from dataclasses import dataclass, field
from typing import (
    TYPE_CHECKING,
    Optional,
    List,
    Dict
)


if TYPE_CHECKING:
    from items import Item


@dataclass
class BodyPart:

    # the name of the part
    name: str

    # a list of parts (by name) that this part is attached to.
    # if this part is deattached, then these parts will be too.
    attachments: list = field(default_factory=lambda: [])

    # a list of greater attachments that this part is attached to.
    # if any part in this list is deattached, then this part will be
    # deattached.
    main_attachments: list = field(default_factory=lambda: [])

    # the status of the body part
    status: str = 'healthy'

    # the weight used in probability checks.
    # the lower the number, the less likely this body part will get
    # targeted
    weight: float = 100

    # if true, will kill the entity instantly if disattached
    is_vital: bool = False

    # can this part hold an item?
    can_hold_item: bool = False

    # can this part be used to attack? (unarmed)
    can_attack_bare: bool = False

    # can this part attack with a weapon?
    can_attack_armed: bool = False

    # the item this part is holding (if can_hold_item)
    held_item: 'Optional[Item]' = None

    # TODO: per-part health

    def get_base_damage(self):
        """Get the damage of the weapon this part is holding, or the damage of
        this body part if it can attack unarmed."""

        if self.can_attack_armed and self.held_item:
            return self.held_item.damage

        elif self.can_attack_bare:
            return 1.0

        else:
            return 0.0


class Body:
    """A representation of parts composing an entitys' body."""

    def __init__(self, game, ent):

        # the game instance
        self.game = game

        # the entity that this body belongs to
        self.owner = ent

        self.parts: Dict[str, BodyPart] = {}

        self.max_health = 100

        self.health = self.max_health

    def is_alive(self) -> bool:
        return self.health > 0

    def get_health_perc(self):
        """Get the health of the body as a percentage."""

        return self.health / self.max_health

    def add_part(self, bodypart: BodyPart):

        self.parts[bodypart.name] = bodypart

    def deattach_part(self, partname: str):

        bodypart = self.parts.get(partname)
        if bodypart:

            self.game.log(self.owner.str_possessive + ' ' + partname + ' has flown off !')
            self.remove_part(bodypart)

    def get_equippable_parts(self) -> List[BodyPart]:
        """Get all body parts that can hold an item."""

        return [part for part in self.parts.values()
                if part.can_hold_item]

    def equip_item(self, part: BodyPart, item: 'Item') -> bool:
        """Set an item to be held by a body part."""

        if part.can_hold_item:
            part.held_item = item
            return True
        else:
            return False

    def get_targetable_parts(self):
        """Get all body parts that can be targeted e.g. not missing."""

        return [part for part in self.parts.values()
                if part.status != 'missing']

    def pick_part(self):
        """Pick a random part of the body using weighted
        probability distribution.

        Use this when not targeting any particular body part.
        """

        parts = self.get_targetable_parts()
        weights = [part.weight for part in parts]

        if len(parts) == 0:
            return None
        else:
            return random.choices(parts, weights)[0]

    def remove_part(self, bodypart: BodyPart):
        """Remove this part and any attachments from the body."""

        bodypart.status = 'missing'
        for partname in bodypart.attachments:
            child = self.parts.get(partname)
            if child:
                self.remove_part(child)

    def hurt(self, damage: int, bodypart=None):

        self.health -= damage

        # choose a random bodypart to target
        bodypart = bodypart or self.pick_part()

        if bodypart is None:
            self.game.log('No body part to target!')

        else:
            # self.deattach_part(bodypart.name)
            # return the bodypart that was damaged
            return bodypart


class HumanoidBody(Body):

    def __init__(self, game, ent):

        super().__init__(game, ent)

        self.add_part(BodyPart("head", [], is_vital=True, weight=10))

        self.add_part(BodyPart("chest", [
            "head", "left_arm", "right_arm", "left_leg", "right_leg"
        ], is_vital=True, weight=100))

        self.add_part(BodyPart("left_arm", ["left_hand"], ["chest"], weight=20))
        self.add_part(BodyPart("left_hand", [], ["left_arm"], weight=5,
            can_attack_armed=True, can_attack_bare=True, can_hold_item=True
        ))

        self.add_part(BodyPart("right_arm", ["right_hand"], ["chest"], weight=20))
        self.add_part(BodyPart("right_hand", [], ["right_arm"], weight=5,
            can_attack_armed=True, can_attack_bare=True, can_hold_item=True
        ))

        self.add_part(BodyPart("left_leg", ["left_foot"], ["chest"], weight=20))
        self.add_part(BodyPart("left_foot", [], ["left_leg"], weight=5))

        self.add_part(BodyPart("right_leg", ["right_foot"], ["chest"], weight=20))
        self.add_part(BodyPart("right_foot", [], ["right_leg"], weight=5))

