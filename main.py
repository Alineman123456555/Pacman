import logging
from time import sleep

from python.coordinate import Coordinate
from python.entity import Wall, Player
from python.world import World, EMPTY_5X5_BOARD
from python.direction import Direction
from python.game import Game
from python.controller import render_world, get_input

logging.basicConfig(level=logging.DEBUG)


def play_game(game: Game):
    """Helper that runs the main loop"""
    game_over = False
    tick_time = 0.25
    while not game_over:
        render_world(game._world)
        sleep(tick_time)
        input = get_input()
        game._tick(input)


# Build World
world = World(Coordinate(10, 10))
world.board[5][5] = Wall()

# Create Game
game = Game(world)
game.add_player(Player(), Coordinate(2, 2))

play_game(game)
