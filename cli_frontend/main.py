"""This file is mainly Temp.
Just to make sure the API works before spending time on the frontend.
"""

import logging
import requests
import urllib.parse
import json
from time import sleep

import python.config as config

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


def get_world_string():
    # TODO: Move to api module
    get_world = urllib.parse.urljoin(config.BASE_URL, config.GET_WORLD)
    logger.info(f"Request url {get_world}")
    world_str_list = requests.get(get_world).json()['game_text_list']
    return "\n".join(world_str_list)


def put_input(m_input: str):
    # TODO: Move to api module
    put_input_url = urllib.parse.urljoin(config.BASE_URL, config.PUT_INPUT)
    logger.info(f"put_input: {m_input}")
    # logger.info(f"Request url {put_input_url}")
    requests.put(put_input_url, json={
        "char": m_input
    })


def put_tick():
    put_tick_url = urllib.parse.urljoin(config.BASE_URL, config.PUT_TICK)
    logger.info(f"Request url {put_tick_url}")
    requests.put(put_tick_url)


def get_input() -> str:
    # TODO: update to use python.util.getch
    import msvcrt

    return msvcrt.getch().decode()


def render_game():
    logger.info("Rendering game")
    with open(config.RENDER_FILE, "w") as f:
        f.write(get_world_string())


def play_game():
    """Helper that runs the main loop"""
    game_over = False
    tick_time = 0.5
    while not game_over:
        render_game()
        sleep(tick_time)
        m_input = get_input()
        put_input(m_input)
        put_tick()
        # try:
        #     NONGAME_BINDS[m_input]()
        # except KeyError:
        #     if game._tick(m_input) != 0:
        #         game_over = True

    # render_gameover(game)
    exit(0)


play_game()

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

# NONGAME_BINDS = {
#     config.QUIT: quit,
#     config.RESTART: GAME.load_game,
# }
