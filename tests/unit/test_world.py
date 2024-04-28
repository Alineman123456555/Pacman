import pytest

from python.world import World


def test_world__init__():
    # TODO: Make better?
    world = World()
    assert world.board == [[None, None], [None, None]]
