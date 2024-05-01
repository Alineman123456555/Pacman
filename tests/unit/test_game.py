import pytest


from python.game import Game


def test_Game__init__():
    game = Game()
    assert game._world.board
    assert game._score == 0


def test_Game_move_player():
    # TODO: Test player movement
    #   Right movement and up movement for the player now teleports
    #   the players as far as possible.
    assert False


def test_Game_move_dumbghost():
    # TODO: Need to test ghost movement
    # When ghost moves up he teleports up and right
    #   then moves down one.
    #   b/c currently he teleports -_-
    assert False
