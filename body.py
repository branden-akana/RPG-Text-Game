
import random


class BodyPart:

    def __init__(
            self,
            name: str,
            attachments: list,
            main_attachments: list = [], *,
            is_vital: bool = False,
            weight: float = 100,
    ):

        # the name of the part
        self.name = name

        # a list of parts (by name) that this part is attached to.
        # if this part is deattached, then these parts will be too.
        self.attachments = attachments

        # a list of greater attachments that this part is attached to.
        # if any part in this list is deattached, then this part will be
        # deattached.
        self.main_attachments = main_attachments

        # if true, will kill the entity instantly if disattached
        self.is_vital = is_vital

        # the status of the body part
        self.status: str = 'healthy'

        self.prob_weight: float = weight

        # TODO: per-part health


class Body:
    """A representation of parts composing an entitys' body."""

    def __init__(self, game, ent):

        # the game instance
        self.game = game

        # the entity that this body belongs to
        self.owner = ent

        self.parts = {}

        self.max_health = 100

        self.health = self.max_health

        self.is_alive = True

    def get_health_perc(self):
        """Get the health of the body as a percentage."""

        return self.health / self.max_health

    def add_part(self, bodypart: BodyPart):

        self.parts[bodypart.name] = bodypart

    def deattach_part(self, partname: str):

        bodypart = self.parts.get(partname)
        if bodypart:

            self.game.add_log(self.owner.str_possessive + ' ' + partname + ' has flown off !')
            self.remove_part(bodypart)

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
        weights = [part.prob_weight for part in parts]

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
            self.game.add_log('No body part to target!')

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
        self.add_part(BodyPart("left_hand", [], ["left_arm"], weight=5))

        self.add_part(BodyPart("right_arm", ["right_hand"], ["chest"], weight=20))
        self.add_part(BodyPart("right_hand", [], ["right_arm"], weight=5))

        self.add_part(BodyPart("left_leg", ["left_foot"], ["chest"], weight=20))
        self.add_part(BodyPart("left_foot", [], ["left_leg"], weight=5))

        self.add_part(BodyPart("right_leg", ["right_foot"], ["chest"], weight=20))
        self.add_part(BodyPart("right_foot", [], ["right_leg"], weight=5))
