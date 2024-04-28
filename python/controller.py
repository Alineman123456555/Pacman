"""This modules handles IO
Taking input from stdin
"rendering" the world to a file.
"""

import logging
from typing import Dict

from python.entity import Entity, Wall, Player
from python.world import World
import python.config as config

logger = logging.getLogger(__name__)

ENTITY_TO_CHAR: Dict[Entity, str] = {type(None): ".", Wall: "X", Player: "0"}


def get_input() -> str:
    # TODO: update to use python.util.getch
    import msvcrt

    return msvcrt.getch().decode()


def space_to_char(space: Entity):
    # TODO: Move to controller
    # TODO: I don't like that spaces are lists
    #   There should only ever really be a single
    #   entity in a space at the end of a tick.
    #   Not sure the best way to represent this?
    #   I guess maybe there could be a temp board each tick.
    #   That stores lists.
    #   After the tick happens there should only be a single
    #   entity in each space.
    return ENTITY_TO_CHAR[space.__class__]


def world_to_string(world: World) -> str:
    # TODO: Move to controller
    # TODO: Probably move to World class
    # Yeah it would be nice for testing? Wait no?
    board = world.board
    world_str = ""
    for row in reversed(board):
        for space in row:
            world_str += space_to_char(space)
        world_str += "\n"

    return world_str


def render_world(world: World):
    """Overwrites the previous file."""
    # File renderer
    # NOTE: Other renderers might need to remove the old output before new is output
    print("rendering")
    with open(config.WORLD_FILE, "w") as f:
        f.write(world_to_string(world))
