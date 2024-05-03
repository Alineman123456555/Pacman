"""This file is mainly Temp.
Just to make sure the API works before spending time on the frontend.
"""

import logging
import requests
import urllib.parse

import python.config as config

logger = logging.getLogger(__name__)


def get_world_string():
    get_world = urllib.parse.urljoin(config.BASE_URL, config.GET_WORLD)
    world_str = requests.get(get_world)


def render_game():
    logger.info("Rendering game")
    with open(config.RENDER_FILE, "w") as f:
        f.write(get_world_string())


render_game()

### This is all commented out while I'm working on it.
#
# def render_game(game: Game):
#     logger.info("Rendering game")
#     with open(config.RENDER_FILE, "w") as f:
#         f.write(game._world_to_string())
#         f.write(f"Score: {game._score}\n")


# def render_gameover(game: Game):
#     world_str = game._world_to_string()

#     # Overwrite chars with gameover
#     world_str = list(world_str)
#     x_len = len(game._world.board) + 1
#     y_len = len(game._world.board[0])
#     gameover = "Game over!"
#     # TODO: Math for placing gameover in the middle is not correct.
#     start = (x_len * y_len // 2) + (y_len // 2) - len(gameover) // 2
#     for idx, char in enumerate(gameover):
#         world_str[idx + start] = char
#     world_str = "".join(world_str)

#     # Render
#     with open(config.RENDER_FILE, "w") as f:
#         f.write(world_str)
#         f.write(f"Score: {game._score}\n")


# def get_input() -> str:
#     # TODO: update to use python.util.getch
#     import msvcrt

#     return msvcrt.getch().decode()


# GAME = Game().load_game()


# NONGAME_BINDS = {
#     config.QUIT: quit,
#     config.RESTART: GAME.load_game,
# }


# def play_game(game: Game):
#     """Helper that runs the main loop"""
#     game_over = False
#     tick_time = 0.25
#     while not game_over:
#         render_game(game)
#         sleep(tick_time)
#         input = get_input()
#         try:
#             NONGAME_BINDS[input]()
#         except KeyError:
#             if game._tick(input) != 0:
#                 game_over = True

#     render_gameover(game)
#     exit(0)


# play_game(GAME)
