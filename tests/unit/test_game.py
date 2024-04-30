import pytest


from python.game import Game


def test_Game__init__():
    game = Game()
    assert game._world.board
    assert game._score == 0
