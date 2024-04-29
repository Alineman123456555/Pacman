import logging
from abc import ABC, abstractmethod
from typing import Tuple, List
from python.coordinate import Coordinate

from python.direction import Direction

logger = logging.getLogger(__name__)


class Entity(ABC):
    pass


class DynamicEntity(Entity):
    def __init__(self):
        self.coords: Coordinate = None
        # TODO: Add world coords.
        raise NotImplementedError

    def gen_move(
        self,
        surroundings: Tuple[
            Entity,
            Entity,
            Entity,
            Entity,
        ],
    ) -> Coordinate:
        """Generates a move

        Parameters
        ----------
        A tuple (length 4 for directions), each index is a List[Entity]

        Returns
        -------
        Tuple[int, int]
            An x, y coordinate in the world.
        """
        # TODO: Refactor surroundings tuple to use a world singleton
        return NotImplementedError


class Player(DynamicEntity):
    def __init__(self, coords: Coordinate = None):
        self.direction: Direction = Direction.NONE
        self.coords: Coordinate = coords

    # TODO: Decide if getters and setters
    #   Makes it easier to avoid AttributeErrors
    # Maybe I should just init entities at (0, 0)
    # or just add a coord to the init

    def gen_move(
        self,
        surroundings: Tuple[
            Entity,
            Entity,
            Entity,
            Entity,
        ],
    ) -> Coordinate:
        # TODO: Figure out if you need to use surroundsing to generate the move.
        return self.coords + self.direction.value


class EatModePlayer(Player):
    def __init__(self, num_ticks: int, coords: Coordinate = None):
        """This class is a player, but interacts differently with Ghosts.
        Parameters
        ----------
        num_ticks: int
            The number of ticks this player should exist.
            Every gen_move() this is decremented
        """
        self._num_ticks = num_ticks
        super().__init__(coords)

    def gen_move(
        self,
        surroundings: Tuple[
            Entity,
            Entity,
            Entity,
            Entity,
        ],
    ) -> Coordinate:
        self._num_ticks -= 1
        logger.debug(f"EatModePlayer num_ticks remaining: {self._num_ticks}")
        return super().gen_move(surroundings)


class Ghost(DynamicEntity):
    pass


class DumbGhost(Ghost):
    def __init__(self, direction: Direction = Direction.UP, coords: Coordinate = None):
        self.direction: Direction = direction
        self.coords: Coordinate = coords

    def gen_move(
        self,
        surroundings: Tuple[
            Entity,
            Entity,
            Entity,
            Entity,
        ],
    ) -> Coordinate:
        # TODO: make logic check all 4 direction no matter what the starting direction is.
        right, left, up, down = surroundings
        if self.direction == Direction.RIGHT and isinstance(right, Wall):
            self.direction = Direction.DOWN
        if self.direction == Direction.DOWN and isinstance(down, Wall):
            self.direction = Direction.LEFT
        if self.direction == Direction.LEFT and isinstance(left, Wall):
            self.direction = Direction.UP
        if self.direction == Direction.UP and isinstance(up, Wall):
            self.direction = Direction.RIGHT

        return self.coords + self.direction.value


class StaticEntity(Entity):
    pass


class Wall(StaticEntity):
    def __init__(self):
        # TODO: Figure out if something needs to be here
        pass


class Interactable(StaticEntity):
    @property
    @abstractmethod
    def value(self):
        """The score value of the interactible"""
        raise NotImplementedError


class SmallDot(Interactable):
    @property
    def value(self):
        return 100


class GhostSpawn(StaticEntity):
    # TODO: Decide if this should be an entity or stored seperately
    #   In the world class.
    def __init__(self):
        raise NotImplementedError
