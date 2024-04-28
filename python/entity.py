from abc import ABC, abstractmethod
from typing import Tuple, List
from python.coordinate import Coordinate

from python.direction import Direction


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
            List["Entity"], List["Entity"], List["Entity"], List["Entity"]
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
        # TODO: Add coords to init parameters
        self.direction: Direction = Direction.NONE
        self.coords: Coordinate = coords

    # TODO: Decide if getters and setters
    #   Makes it easier to avoid AttributeErrors
    # Maybe I should just init entities at (0, 0)
    # or just add a coord to the init

    def gen_move(self, surroundings: Tuple[List[Entity]]) -> Coordinate:
        # TODO: Figure out if you need to use surroundsing to generate the move.
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
