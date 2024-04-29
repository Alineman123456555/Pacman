"""This modules handles IO
Taking input from stdin
"rendering" the world to a file.
"""

import logging

from typing import Dict, List

from python.entity import (
    Entity,
    Wall,
    Player,
    SmallDot,
    DumbGhost,
    EatModePlayer,
    DynamicEntity,
)
from python.world import World, gen_empty_board
from python.game import Game
from python.coordinate import Coordinate
import python.config as config

logger = logging.getLogger(__name__)

ENTITY_TO_CHAR: Dict[Entity, str] = {
    type(None): ".",
    Wall: "X",
    Player: "O",
    SmallDot: "-",
    DumbGhost: "G",
    EatModePlayer: "0",
}

CHAR_TO_ENTITY: Dict[Entity, str] = {
    ".": type(None),
    "X": Wall,
    "O": Player,
    "-": SmallDot,
    "G": DumbGhost,
    "0": EatModePlayer,
}


def get_input() -> str:
    # TODO: update to use python.util.getch
    import msvcrt

    return msvcrt.getch().decode()


def space_to_char(space: Entity):
    return ENTITY_TO_CHAR[space.__class__]


def world_to_string(world: World) -> str:
    # TODO: Probably move to World class
    # Yeah it would be nice for testing? Wait no?
    board = world.board

    y_str_list = [""] * len(board[0])
    for column in board:
        for yidx, space in enumerate(reversed(column)):
            y_str_list[yidx] += space_to_char(space)

    return "\n".join(y_str_list) + "\n"


def render_world(world: World):
    """Overwrites the previous file."""
    # File renderer
    # NOTE: Other renderers might need to remove the old output before new is output
    print("rendering")
    with open(config.RENDER_FILE, "w") as f:
        f.write(world_to_string(world))


def render_gameover(game: Game):
    world_str = world_to_string(game._world)

    # Overwrite chars with gameover
    world_str = list(world_str)
    x_len = len(game._world.board) + 1
    y_len = len(game._world.board[0])
    gameover = "Game over!"
    start = (x_len * y_len // 2) + (y_len // 2) - len(gameover) // 2
    for idx, char in enumerate(gameover):
        world_str[idx + start] = char
    world_str = "".join(world_str)

    # Render
    with open(config.RENDER_FILE, "w") as f:
        f.write(world_str)
        f.write(f"Score: {game._score}\n")


def render_game(game: Game):
    logger.info("Rendering game")
    with open(config.RENDER_FILE, "w") as f:
        f.write(world_to_string(game._world))
        f.write(f"Score: {game._score}\n")


def load_board(filename: str) -> List[List[Entity]]:
    board_str = ""
    with open(filename, "r") as f:
        board_str = f.read().strip()

    row_list = board_str.split("\n")
    y_size = len(row_list)
    x_size = len(row_list[0])

    board = gen_empty_board(Coordinate(x_size, y_size))
    logger.debug(f"Empty board size x: {len(board)}, y: {len(board[0])}")
    for yidx, row in enumerate(reversed(row_list)):
        logger.debug(f"Row: '{row}', len: {len(row)}")
        for xidx, char in enumerate(row):
            logger.debug(f"Loading char: {char}, xidx: {xidx}, yidx: {yidx}")
            entity = CHAR_TO_ENTITY[char]()
            if isinstance(entity, DynamicEntity):
                entity.coords = Coordinate(xidx, yidx)
            board[xidx][yidx] = entity

    return board
