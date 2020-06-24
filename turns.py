
from entity import LivingEntity
from typing import (
    List,
    TYPE_CHECKING
)


if TYPE_CHECKING:
    from game import Game


class TurnManager:
    """A manager for the turn order of entities."""

    def __init__(self, game: 'Game', ents: 'List[LivingEntity]'):

        self.game = game
        self.ents = ents
        self.order = []
        self.idx = 0
        self.last_idx = 0

    def start_order(self):
        """Decide the turn order of the given list of entities."""

        # for now just use the same order as the list
        order = [ent for ent in self.ents
                if isinstance(ent, LivingEntity)]

        # if len(order):
            # self.game.info(f'** order: {[ent.get_name() for ent in order]} **')

        self.idx = 0
        self.last_idx = 0
        self.order = order

    def get_last_entity(self) -> LivingEntity:
        return self.order[self.last_idx]

    def get_current_entity(self) -> LivingEntity:
        return self.order[self.idx]

    def run_next(self):
        """Run the next turn in the order."""

        if len(self.order) > 0:

            ent = self.order[self.idx]

            if ent.is_alive():
                # self.game.info(f'it is now {ent.get_name()} turn')
                action = ent.think()
                if action: action.do_action()

            # increment index
            self.last_idx = self.idx
            self.idx = (self.idx + 1) % len(self.order)
