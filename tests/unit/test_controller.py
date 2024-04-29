import pytest
import os

from python.controller import (
    space_to_char,
    world_to_string,
    render_world,
    render_gameover,
    render_game,
)
from python.coordinate import Coordinate
from python.game import Game
from python.world import World, gen_empty_board
from python.entity import Wall
from python.config import WORLD_FILE


def test_space_to_char():
    assert space_to_char(Wall()) == "X"
    assert space_to_char(None) == "."


def test_world_to_string():
    world = World()
    world.board = gen_empty_board(Coordinate(4, 1))
    assert world_to_string(world) == "....\n"

    world.board = [[Wall()], [None], [Wall()], [None]]
    assert world_to_string(world) == "X.X.\n"

    world.board = [[Wall(), None, Wall(), None]]
    assert world_to_string(world) == ".\nX\n.\nX\n"

    world.board = [[Wall(), None, None, None]]
    assert world_to_string(world) == ".\n.\n.\nX\n"


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


def test_render_gameover(pytester):
    tempdir = pytester.path
    os.chdir(tempdir)
    world_file = os.path.abspath(WORLD_FILE)
    world = World()
    game = Game(world)
    with pytest.raises(IndexError):
        render_gameover(game)

    world.board = gen_empty_board(Coordinate(10, 1))
    render_gameover(game)
    with open(world_file, "r") as f:
        result = f.read()
    assert result == "Game over!\nScore: 0\n"


def test_render_game(pytester):
    tempdir = pytester.path
    os.chdir(tempdir)
    world_file = os.path.abspath(WORLD_FILE)
    world = World()
    game = Game(world)
    render_game(game)
    with open(world_file, "r") as f:
        result = f.read()
    assert result == ".\nScore: 0\n"
