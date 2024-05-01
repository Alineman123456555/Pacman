import pytest

from python.direction import Direction
from python.coordinate import Coordinate
from python.entity import Interactable, SmallDot, DumbGhost, Player, Wall


def test_Interactable():
    with pytest.raises(TypeError):
        Interactable()


def test_SmallDot():
    assert SmallDot().value == 100


def test_Player():
    assert False


def test_Player_gen_move():
    player = Player()
    player.direction = Direction.UP
    player.coords = Coordinate(4, 4)
    assert player.gen_move({}) == Coordinate(4, 5)
    player.direction = Direction.RIGHT
    assert player.gen_move({}) == Coordinate(5, 4)
    player.direction = Direction.LEFT
    assert player.gen_move({}) == Coordinate(3, 4)
    player.direction = Direction.DOWN
    assert player.gen_move({}) == Coordinate(4, 3)


def test_DumbGhost():
    assert False


def test_DumbGhost_gen_move():
    # TODO: Need to test ghost movement
    # When ghost moves up he teleports up and right
    #   then moves down one.
    #   b/c currently he teleports -_-
    assert False
