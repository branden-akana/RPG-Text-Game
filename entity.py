
import typing
import body


if typing.TYPE_CHECKING:
    from game import Game


class Entity:
    """Represents an entity."""

    def __init__(self, game: 'Game', name: str):

        # a reference to the game
        self.game: 'Game' = game

        # the name of the entity
        self.name = name


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
        return self.body.is_alive
