import logging
from typing import Dict, List
from time import sleep

from python.entity import Entity, Wall, Player, DynamicEntity
from python.world import World, gen_empty_board
from python.config import WORLD_FILE
from python.direction import Direction
from python.coordinate import Coordinate
import python.config as config

logger = logging.getLogger(__name__)

ENTITY_TO_CHAR: Dict[Entity, str] = {type(None): ".", Wall: "X", Player: "0"}


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
    with open(WORLD_FILE, "w") as f:
        f.write(world_to_string(world))


def get_input() -> str:
    # TODO: update to use python.util.getch
    import msvcrt

    return msvcrt.getch().decode()


# TODO: Create game class
#   Class has a tick function that does a number of things
#   1. Move all entities (tmp board)
#   2. Check the game state
#   3. Update the board
# This class also tracks scoring and other random things like that


def get_player(world: World) -> Player:
    # This kinda sucks.
    #   Might want to store the player seperate or add some better way to get the player.
    return list(world.dynamic_entities)[0]


DIRECTION_BINDS = {
    config.MOVE_UP: Direction.UP,
    config.MOVE_DOWN: Direction.DOWN,
    config.MOVE_LEFT: Direction.LEFT,
    config.MOVE_RIGHT: Direction.RIGHT,
}


def update_player_velocity(player: Player, direction: Direction):
    # TODO: Refactor to game class
    #   So you don't have to pass player in.
    player.direction = direction


def is_valid_move(world: World, coord: Coordinate):
    # TODO: Refactor all of this to game class.
    #   So that you don't have to pass the world in to function.
    # TODO: Refactor so player and ghosts use different
    #   is_valid_move functions.
    #   this is b/c the logic for both types of entities is different.
    """
    The only type of entity you can't move onto is a Wall
    """
    if isinstance(world.get_entity(coord), Wall):
        return False
    else:
        return True


class Game:
    def __init__(self, world: World = World(Coordinate(0, 0))) -> None:
        self._world = world
        self._score = 0
        self._player = None

    def add_player(self, player: Player, coord: Coordinate):
        self._world.place_entity(player, coord)
        self._player = player

    def play_game(self):
        game_over = False
        tick_time = 1
        player = get_player(self._world)
        while not game_over:
            render_world(self._world)
            sleep(tick_time)
            input = get_input()
            self._tick(player, input)

    def _tick(self, player: Player, input):
        # Get input from controller (cli)
        # Async??
        update_player_velocity(player, DIRECTION_BINDS[input])
        # Create empty tmp_board with List[Entity] spaces

        # All DynamicEntities move
        #   New positions are stored in the tmp_board
        tmp_board: List[List[List[Entity]]] = gen_empty_board(
            # TODO: This tmp_board needs to include interactables -_-
            # TODO: Improve how this call works for generating a temp board :(
            Coordinate(len(self._world.board), len(self._world.board[0])),
            list().copy,
        )
        # Check the game state
        #   Check game_over
        #   Delete things update world.board

        # Move all DynamicEntities
        for dyent in self._world.dynamic_entities:
            print(dyent)
            new_coords = dyent.gen_move(None)
            # TODO: Add is_valid_move(new_coords)
            #   Maybe old coords should also be passed to is_valid_move?
            if is_valid_move(self._world, new_coords):
                tmp_board[new_coords.x][new_coords.y].append(dyent)
            else:
                logger.info(f"Can't move entity, to {new_coords}")
            # TODO: This should store the entity in the tmp_board

        # Update board
        # TODO: Refactor
        self._update_world(tmp_board)

    def _update_world(self, tmp_board):
        for x, row in enumerate(tmp_board):
            for y, entity_list in enumerate(row):
                for entity in entity_list:
                    if isinstance(entity, DynamicEntity):
                        self._world.move_entity(entity, Coordinate(x, y))
