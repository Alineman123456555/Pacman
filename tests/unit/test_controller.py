import pytest
import os

from python.controller import (
    space_to_char,
    world_to_string,
    render_world,
    render_gameover,
    render_game,
    load_board,
)
from python.coordinate import Coordinate
from python.game import Game
from python.world import World
from python.entity import Wall, Player, SmallDot
from python.config import RENDER_FILE


def test_space_to_char():
    assert space_to_char(Wall()) == "X"
    assert space_to_char(None) == "."


def test_world_to_string():
    world = World()
    world.board = World.gen_empty_board(Coordinate(4, 1))
    assert world_to_string(world) == "....\n"

    world.board = [[{Wall()}], [set()], [{Wall()}], [set()]]
    assert world_to_string(world) == "X.X.\n"

    world.board = [[{Wall()}, set(), {Wall()}, set()]]
    assert world_to_string(world) == ".\nX\n.\nX\n"

    world.board = [[{Wall()}, set(), set(), set()]]
    assert world_to_string(world) == ".\n.\n.\nX\n"


def test_render_world(pytester):
    tempdir = pytester.path
    os.chdir(tempdir)
    world_file = os.path.abspath(RENDER_FILE)

    world = World(Coordinate(2, 2))
    render_world(world)
    with open(world_file, "r") as f:
        result = f.read()
    assert result == "..\n..\n"

    world.board = [[{Wall()}, {Wall()}], [{Wall()}, {Wall()}]]
    render_world(world)
    with open(world_file, "r") as f:
        result = f.read()
    assert result == "XX\nXX\n"


def test_render_gameover(pytester):
    tempdir = pytester.path
    os.chdir(tempdir)
    world_file = os.path.abspath(RENDER_FILE)
    world = World()
    game = Game(world)
    with pytest.raises(IndexError):
        render_gameover(game)

    world.board = World.gen_empty_board(Coordinate(10, 1))
    render_gameover(game)
    with open(world_file, "r") as f:
        result = f.read()
    assert result == "Game over!\nScore: 0\n"


def test_render_game(pytester):
    tempdir = pytester.path
    os.chdir(tempdir)
    world_file = os.path.abspath(RENDER_FILE)
    world = World()
    game = Game(world)
    render_game(game)
    with open(world_file, "r") as f:
        result = f.read()
    assert result == ".\nScore: 0\n"


def test_load_board(pytester):
    tempdir = pytester.path

    world_file = os.path.join(tempdir, "world_file.txt")
    with open(world_file, "w") as f:
        f.write(".-.\n" "OX.\n")

    board = load_board(world_file)

    assert isinstance(list(board[0][0])[0], Player)
    assert isinstance(list(board[1][0])[0], Wall)
    assert list(board[2][0])[0] is None
    assert list(board[0][1])[0] is None
    assert isinstance(list(board[1][1])[0], SmallDot)
    assert list(board[2][1])[0] is None
