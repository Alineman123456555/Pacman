import logging

from python.coordinate import Coordinate
from python.entity import Wall, Player
from python.world import World, EMPTY_5X5_BOARD
from python.direction import Direction
from python.game import play_game

logging.basicConfig(level=logging.DEBUG)

world = World(Coordinate(10, 10))
world.board[5][5] = Wall()
world.place_entity(Player(), Coordinate(2, 2))

play_game(world)
