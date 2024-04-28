from enum import Enum

from python.coordinate import Coordinate

# TODO: Add map for


class Direction(Enum):
    # Defines the coordinate direction
    RIGHT = Coordinate(0, 1)
    LEFT = Coordinate(0, -1)
    UP = Coordinate(1, 0)
    DOWN = Coordinate(-1, 0)
    NONE = Coordinate(0, 0)
    # TODO: Add succ and pred functions?
