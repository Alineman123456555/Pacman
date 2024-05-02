import pytest

from python.coordinate import Coordinate


def test_coordinate():
    coord = Coordinate(1, 3)
    assert coord.x == 1
    assert coord.y == 3


def test_coordinate_add():
    coord_1 = Coordinate(1, 2)
    coord_2 = Coordinate(2, 5)

    result = coord_1 + coord_2
    assert result.x == 3
    assert result.y == 7

    zero_coord = Coordinate(0, 0)
    result = coord_1 + zero_coord
    assert result.x == coord_1.x
    assert result.y == coord_1.y
