import logging
from typing import Dict, List, Set


from python.entity import Entity, Wall, Player, DynamicEntity
from python.world import World, gen_empty_board
from python.direction import Direction
from python.coordinate import Coordinate
import python.config as config

logger = logging.getLogger(__name__)


# This class also tracks scoring and other random things like that


DIRECTION_BINDS = {
    config.MOVE_UP: Direction.UP,
    config.MOVE_DOWN: Direction.DOWN,
    config.MOVE_LEFT: Direction.LEFT,
    config.MOVE_RIGHT: Direction.RIGHT,
}


class Game:
    def __init__(self, world: World = World(Coordinate(0, 0))) -> None:
        self._world = world
        self._score = 0
        self._player = None
        self._dynamic_entities: Set[DynamicEntity] = set()

    def add_player(self, player: Player, coord: Coordinate):
        self._world.place_entity(player, coord)
        self._player = player
        self._dynamic_entities.add(player)

    def _tick(self, input):
        # Get input from controller (cli)
        # Async??
        self._update_player_velocity(DIRECTION_BINDS[input])
        # TODO: Handle KeyError
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
        for dyent in self._dynamic_entities:
            print(dyent)
            new_coords = dyent.gen_move(None)
            # TODO: Add is_valid_move(new_coords)
            #   Maybe old coords should also be passed to is_valid_move?
            if self._is_valid_move(new_coords):
                tmp_board[new_coords.x][new_coords.y].append(dyent)
            else:
                logger.info(f"Can't move entity, to {new_coords}")
            # TODO: This should store the entity in the tmp_board

        # Update board
        # TODO: Refactor
        self._update_world(tmp_board)

    def _update_player_velocity(self, direction: Direction):
        self._player.direction = direction

    def _is_valid_move(self, coord: Coordinate):
        # TODO: Refactor so player and ghosts use different
        #   is_valid_move functions.
        #   this is b/c the logic for both types of entities is different.
        """
        The only type of entity you can't move onto is a Wall
        """
        if isinstance(self._world.get_entity(coord), Wall):
            return False
        else:
            return True

    def _update_world(self, tmp_board):
        for x, row in enumerate(tmp_board):
            for y, entity_list in enumerate(row):
                for entity in entity_list:
                    if isinstance(entity, DynamicEntity):
                        self._world.move_entity(entity, Coordinate(x, y))
