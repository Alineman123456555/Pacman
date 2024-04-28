import pytest
import os

from python.game import space_to_char, world_to_string, render_world
from python.entity import Wall
from python.world import World
from python.config import WORLD_FILE


def test_space_to_char():
    assert space_to_char(Wall()) == "X"
    assert space_to_char(None) == " "


def test_world_to_string():
    world = World()

    # Check that world coords are displayed correctly
    world.board = [[Wall(), Wall()], [Wall(), Wall()]]
    assert world_to_string(world) == "XX\nXX\n"
    world.board = [[None, Wall()], [Wall(), Wall()]]
    assert world_to_string(world) == "XX\n X\n"
    world.board = [[Wall(), None], [Wall(), Wall()]]
    assert world_to_string(world) == "XX\nX \n"


def test_render_world(pytester):
    tempdir = pytester.path
    os.chdir(tempdir)
    world_file = os.path.abspath(WORLD_FILE)

    world = World()
    render_world(world)
    with open(world_file, "r") as f:
        result = f.read()
    assert result == "  \n  \n"

    world.board = [[Wall(), Wall()], [Wall(), Wall()]]
    render_world(world)
    with open(world_file, "r") as f:
        result = f.read()
    assert result == "XX\nXX\n"
