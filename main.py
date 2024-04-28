import logging
from time import sleep

from python.coordinate import Coordinate
from python.entity import Wall, Player
from python.world import World, EMPTY_5X5_BOARD
from python.direction import Direction
from python.game import Game
from python.controller import render_world, get_input
import python.config as config

logging.basicConfig(level=logging.DEBUG)


def create_world():
    # TODO: Move to world?
    world = World(Coordinate(10, 10))
    world.board[5][5] = Wall()
    return world


def create_game():
    # TODO: Move to game
    # Build World
    world = create_world()

    # Create Game
    game = Game(world)
    game.add_player(Player(), Coordinate(2, 2))

    return game


GAME = create_game()


def restart_game(game: Game = GAME):
    # TODO: Move to Game class
    #   And rename to something like
    #   set_game_state?
    game._world = create_world()
    game._dynamic_entities = set()
    game.add_player(Player(), Coordinate(2, 2))


NONGAME_BINDS = {
    config.QUIT: quit,
    config.RESTART: restart_game,
}


def play_game(game: Game):
    """Helper that runs the main loop"""
    game_over = False
    tick_time = 0.25
    while not game_over:
        render_world(game._world)
        sleep(tick_time)
        input = get_input()
        try:
            NONGAME_BINDS[input](game)
        except KeyError:
            game._tick(input)


play_game(GAME)
