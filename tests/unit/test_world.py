import pytest

from python.coordinate import Coordinate
from python.world import gen_empty_board, World
from python.entity import Player


def test_gen_empty_board():
    # TODO: Implement?
    pass


def test_world__init__():
    # TODO: Make better?
    world = World(Coordinate(2, 2))
    assert world.board == [[None, None], [None, None]]


def test_world_move_entity():
    # TODO: Implement?
    world = World(Coordinate(2, 2))
    pass


def test_place_entity():
    player = Player()
    world = World(Coordinate(3, 3))

    world.place_entity(player, Coordinate(1, 1))
    assert world.board == [
        [None, None, None],
        [None, player, None],
        [None, None, None],
    ]
