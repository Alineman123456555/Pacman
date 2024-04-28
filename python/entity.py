from abc import ABC, abstractmethod
from typing import Tuple, List
from dataclasses import dataclass

from python.direction import Direction


@dataclass
class Coordinate:
    x: int
    y: int

    def __add__(self, other: "Coordinate"):
        n_x = self.x + other.x
        n_y = self.y + other.y
        return Coordinate(n_x, n_y)


class Entity(ABC):
    def __init__(self):
        raise NotImplementedError


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
    def __init__(self):
        # TODO: Add coords to init parameters
        self.direction: Direction = Direction.NONE
        self.coords: Tuple[int, int] = None

    # TODO: Decide if getters and setters
    #   Makes it easier to avoid AttributeErrors
    # Maybe I should just init entities at (0, 0)
    # or just add a coord to the init

    def gen_move(self, surroundings: Tuple[List[Entity]]) -> Tuple[int]:
        # TODO: Figure out if you need to use surroundsing to generate the move.
        return self.coords + self.direction


class StaticEntity(Entity):
    def __init__(self):
        raise NotImplementedError


class Wall(StaticEntity):
    def __init__(self):
        # TODO: Figure out if something needs to be here
        pass


class GhostSpawn(StaticEntity):
    # TODO: Decide if this should be an entity or stored seperately
    #   In the world class.
    def __init__(self):
        raise NotImplementedError
