from typing import Dict, List
from time import sleep

from python.entity import Entity, Wall, Player
from python.world import World
from python.config import WORLD_FILE

ENTITY_TO_CHAR: Dict[Entity, str] = {type(None): " ", Wall: "X", Player: "0"}


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
    with open(WORLD_FILE, "w") as f:
        f.write(world_to_string(world))


# TODO: Create game class
#   Class has a tick function that does a number of things
#   1. Move all entities (tmp board)
#   2. Check the game state
#   3. Update the board
# This class also tracks scoring and other random things like that


def play_game(world: World):
    game_over = False
    tick_time = 2
    tmp = False
    while not game_over:
        # Get input from controller (cli)
        # Async??
        # Create empty tmp_board with List[Entity] spaces

        # All DynamicEntities move
        #   New positions are stored in the tmp_board
        # Check the game state
        #   Check game_over
        #   Delete things update world.board

        # Render world
        # if tmp:
        #     world.board = [[Wall(), Wall()], [Wall(), Wall()]]
        # else:
        #     world.board = [[None, None], [None, None]]

        # Move all DynamicEntities
        for dyent in world.dynamic_entities:
            new_coords = dyent.gen_move(None)
            # TODO: Add is_valid_move(new_coords)
            #   Maybe old coords should also be passed to is_valid_move?
            world.move_entity(dyent, new_coords)

        render_world(world)
        sleep(tick_time)
        # tmp = not tmp
