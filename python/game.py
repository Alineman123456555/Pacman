import logging

from typing import Dict, List, Set

from python.entity import (
    Entity,
    Wall,
    Player,
    DynamicEntity,
    Interactable,
    Ghost,
)
from python.world import World
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
    def __init__(self, world: World = World(Coordinate(1, 1))) -> None:
        self._world = world
        self._score = 0
        self._player = None

    def add_player(self, player: Player, coord: Coordinate):
        self._world.place_dynamic_entity(player, coord)
        self._player = player

    def add_dynamic_entity(self, entity: Entity, coord: Coordinate):
        self._world.place_dynamic_entity(entity, coord)

    def _tick(self, input) -> int:
        # Get input from controller (cli)
        # TODO: Make async
        try:
            self._update_player_velocity(DIRECTION_BINDS[input])
        except KeyError:
            logger.warning(f"Unknown Direction Keybind: {input}")

        # All things move on this board first
        # TODO: Figure out if you need a temp_world,
        #   now that each cell can store as many entities as it wants.
        # temp_world = World(self._world.size)

        # Move all Entities
        # self._move_entities(temp_world)
        # TODO: Right movement and up movement for the player now teleports
        #   the players as far as possible.
        # TODO: When ghost moves up he teleports up and right
        #   then moves down one.
        #   THIS ALL STARTED HAPPENING AFTER REMOVING THE TEMP WORLD.

        self._move_entities(self._world)

        # Perform actions for entities on same spot
        self._interact_entities(self._world)

        # Update board
        # self._update_world(temp_world)

        # Check if game is over
        # TODO: Refactor
        if not self._player:
            logger.error("No player!")
            # TODO: Add respawn
            return 1
        return 0

    def _move_entities(self, temp_world: World):
        for old_coords, cell in self._world.enumerate():
            dyent: DynamicEntity
            for dyent in cell.get_subclass_set(DynamicEntity):
                new_coords = dyent.gen_move(self._world.get_surroundings(old_coords))
                if not self._is_valid_move(new_coords):
                    logger.info(f"Can't move entity, to {new_coords}")
                    new_coords = old_coords
                temp_world.move_dynamic_entity(dyent, new_coords)
                # TODO: Remove if temp_world is unneccessary
                # temp_world.add_entity(dyent, new_coords)

    def _update_player_velocity(self, direction: Direction):
        self._player.direction = direction

    def _is_valid_move(self, coord: Coordinate):
        # TODO: Refactor so player and ghosts use different
        #   is_valid_move functions.
        #   this is b/c the logic for both types of entities is different.
        """
        The only type of entity you can't move onto is a Wall
        """
        cell = self._world.get_cell(coord)
        if cell.has_class(Wall):
            return False
        return True

    def _interact_entities(self, temp_world: World):
        for coords, cell in temp_world.enumerate():
            if cell.has_subclass(Player):
                # Player, Interactable interaction
                if cell.has_subclass(Interactable):
                    # TODO: FIX THIS
                    #   Currently temp_world doesn't include interactables -_-
                    #   Maybe add copy constructor to world.
                    #
                    logger.info(f"Player, Interactable interaction")
                    interactable: Interactable
                    for interactable in cell.get_subclass_set(Interactable):
                        self._score += interactable.value
                        # TODO: Remove interactable after interaction
                # Player, Ghost interaction
                if cell.has_subclass(Ghost):
                    logger.info(f"Player, Ghost interaction")
                    for player in cell.get_subclass_set(Player):
                        self._player = None
                        temp_world.remove_dynamic_entity(player)

        # TODO: Add game logic for entity interactions

    def _update_world(self, temp_world: World):
        # TODO: Figure out if there's a good way to
        #   Just update the world with a new board.
        # self._world.board = tmp_board
        for coords, cell in temp_world.enumerate():
            for dyent in cell.get_subclass_set(DynamicEntity):
                self._world.move_dynamic_entity(dyent, coords)
