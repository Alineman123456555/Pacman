import pytest

from python.coordinate import Coordinate
from python.world import World
from python.entity import Player


def test_gen_empty_board():
    with pytest.raises(ValueError):
        World.gen_empty_board(Coordinate(0, 0))

    assert World.gen_empty_board(Coordinate(2, 1)) == [[set()], [set()]]


def test_world__init__():
    # TODO: Make better?
    world = World(Coordinate(2, 2))
    assert world.board == [[set(), set()], [set(), set()]]


def test_world_move_entity():
    # TODO: Implement?
    world = World(Coordinate(2, 2))
    pass


def test_place_entity():
    player = Player()
    world = World(Coordinate(3, 3))

    world.place_dynamic_entity(player, Coordinate(1, 1))
    assert world.board == [
        [set(), set(), set()],
        [set(), {player}, set()],
        [set(), set(), set()],
    ]
