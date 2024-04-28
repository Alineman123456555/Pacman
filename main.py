import logging
from time import sleep

from python.coordinate import Coordinate
from python.entity import Wall, Player, SmallDot, DumbGhost
from python.world import World
from python.direction import Direction
from python.game import Game
from python.controller import render_game, get_input, render_gameover
import python.config as config

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)


def create_wall(world: World, start: Coordinate, end: Coordinate):
    logger.debug(f"Creating wall start: {start}, end: {end}")
    for x in range(start.x, end.x + 1):
        for y in range(start.y, end.y + 1):
            logger.debug(f"Creating wall at x: {x}, y: {y}")
            world.board[x][y] = Wall()


def create_world():
    # TODO: Move to world?
    world = World(Coordinate(40, 100))

    # Left wall
    create_wall(world, Coordinate(5, 5), Coordinate(5, 9))

    # Right wall
    create_wall(world, Coordinate(10, 5), Coordinate(10, 9))

    # Bottom wall
    create_wall(world, Coordinate(6, 5), Coordinate(9, 5))

    # Top wall
    create_wall(world, Coordinate(6, 9), Coordinate(9, 9))

    world.board[3][7] = SmallDot()

    return world


def create_game():
    # TODO: Move to game
    # Build World
    world = create_world()

    # Create Game
    game = Game(world)
    game.add_player(Player(), Coordinate(7, 8))
    game.add_dynamic_entity(DumbGhost(Direction.UP), Coordinate(7, 7))

    return game


GAME = create_game()


def restart_game(game: Game = GAME):
    # TODO: Move to Game class
    #   And rename to something like
    #   set_game_state?
    game._world = create_world()
    game.add_player(Player(), Coordinate(2, 2))
    game._score = 0


NONGAME_BINDS = {
    config.QUIT: quit,
    config.RESTART: restart_game,
}


def play_game(game: Game):
    """Helper that runs the main loop"""
    game_over = False
    tick_time = 0.25
    while not game_over:
        render_game(game)
        sleep(tick_time)
        input = get_input()
        try:
            NONGAME_BINDS[input](game)
        except KeyError:
            if game._tick(input) != 0:
                game_over = True

    render_gameover(game)
    exit(0)


play_game(GAME)
