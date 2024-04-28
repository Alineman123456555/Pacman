import logging

from python.coordinate import Coordinate
from python.entity import Wall, Player
from python.world import World, EMPTY_5X5_BOARD
from python.direction import Direction
from python.game import Game

logging.basicConfig(level=logging.DEBUG)

# Build World
world = World(Coordinate(10, 10))
world.board[5][5] = Wall()

# Create Game
game = Game(world)
game.add_player(Player(), Coordinate(2, 2))
game.play_game()
