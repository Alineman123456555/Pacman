import pytest
import os

from python.game import Game
from python.coordinate import Coordinate
from python.entity import Wall
from python.world import World


def test_Game__init__():
    game = Game()
    assert game._world.board == [[None]]
    assert game._score == 0

    world = World(Coordinate(2, 2))
    game = Game(world)
    assert game._world.board == [[None, None], [None, None]]
