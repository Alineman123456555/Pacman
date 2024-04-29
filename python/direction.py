from enum import Enum

from python.coordinate import Coordinate

# TODO: Add map for


class Direction(Enum):
    # Defines the coordinate direction
    UP = Coordinate(0, 1)
    DOWN = Coordinate(0, -1)
    RIGHT = Coordinate(1, 0)
    LEFT = Coordinate(-1, 0)
    NONE = Coordinate(0, 0)
    # TODO: Add succ and pred functions?
