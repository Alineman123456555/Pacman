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
        # Async??
        try:
            self._update_player_velocity(DIRECTION_BINDS[input])
        except KeyError:
            logger.warning(f"Unknown Direction Keybind: {input}")

        # All things move on this board first
        temp_world = World(self._world.size)

        # Move all Entities
        self._move_entities(temp_world)

        # Perform actions for entities on same spot
        # self._interact_entities(temp_world)

        # Update board
        self._update_world(temp_world)
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
                temp_world.add_entity(dyent, new_coords)

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

    def _space_to_class_entity_set_dict(
        self,
        entity_set: Set[Entity],
    ) -> Dict[type, Set[Entity]]:
        # TODO: Refactor to world class, actually a new Space class would be good
        class_dict: Dict[type, Set[Entity]] = {}
        for entity in entity_set:
            class_dict.setdefault(entity.__class__, set())
            class_dict[entity.__class__].add(entity)
        return class_dict

    def _dict_has(
        self, entity_class_dict: Dict[type, Set[Entity]], class_type: type
    ) -> bool:
        # TODO: Feel like this should get moved to a space class.
        # TODO: Move to entity module
        for entity_class in entity_class_dict.keys():
            if issubclass(entity_class, class_type):
                return True
        return False

    def _dict_get(
        self, entity_class_dict: Dict[type, Set[Entity]], class_type: type
    ) -> Set[Entity]:
        # TODO: Feel like this should get moved to a space class.
        full_entity_set = set()
        for entity_class, entity_set in entity_class_dict.items():
            if issubclass(entity_class, class_type):
                full_entity_set.update(entity_set)
        return full_entity_set

    def _interact_entities(self, tmp_board: List[List[Set[Entity]]]):
        for coords, entity_set in World.enumerate(tmp_board):
            # Setup
            class_dict = self._space_to_class_entity_set_dict(entity_set)

            # Player Interactable interaction
            if self._dict_has(class_dict, Interactable) and self._dict_has(
                class_dict, Player
            ):
                interactable: Interactable
                for interactable in self._dict_get(class_dict, Interactable):
                    self._score += interactable.value
                    # TODO: Remove interactable after interaction.

            # Player Ghost interaction
            if self._dict_has(class_dict, Ghost) and self._dict_has(class_dict, Player):
                # TODO: Add player eat mode.
                for player in self._dict_get(class_dict, Player):
                    if player == self._player:
                        self._player = None
                        tmp_board[coords.x][coords.y].remove(player)

        # TODO: Add game logic for entity interactions

    def _update_world(self, temp_world: World):
        # TODO: Figure out if there's a good way to
        #   Just update the world with a new board.
        # self._world.board = tmp_board
        for coords, cell in temp_world.enumerate():
            for dyent in cell.get_subclass_set(DynamicEntity):
                self._world.move_dynamic_entity(dyent, coords)
