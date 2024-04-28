from enum import Enum


class Direction(Enum):
    # Defines the coordinate direction
    UP = (0, 1)
    DOWN = (0, -1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    NONE = (0, 0)
    # TODO: Add succ and pred functions?
