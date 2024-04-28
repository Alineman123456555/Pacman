import pytest
import os

from python.game import space_to_char, world_to_string, render_world, Game
from python.coordinate import Coordinate
from python.entity import Wall
from python.world import World
from python.config import WORLD_FILE


def test_space_to_char():
    assert space_to_char(Wall()) == "X"
    assert space_to_char(None) == "."


def test_world_to_string():
    world = World(Coordinate(2, 2))

    # Check that world coords are displayed correctly
    world.board = [[Wall(), Wall()], [Wall(), Wall()]]
    assert world_to_string(world) == "XX\nXX\n"
    world.board = [[None, Wall()], [Wall(), Wall()]]
    assert world_to_string(world) == "XX\n.X\n"
    world.board = [[Wall(), None], [Wall(), Wall()]]
    assert world_to_string(world) == "XX\nX.\n"


def test_render_world(pytester):
    tempdir = pytester.path
    os.chdir(tempdir)
    world_file = os.path.abspath(WORLD_FILE)

    world = World(Coordinate(2, 2))
    render_world(world)
    with open(world_file, "r") as f:
        result = f.read()
    assert result == "..\n..\n"

    world.board = [[Wall(), Wall()], [Wall(), Wall()]]
    render_world(world)
    with open(world_file, "r") as f:
        result = f.read()
    assert result == "XX\nXX\n"


def test_Game__init__():
    game = Game()
    assert game._world.board == []
    assert game._score == 0

    world = World(Coordinate(2, 2))
    game = Game(world)
    assert game._world.board == [[None, None], [None, None]]
