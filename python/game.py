import logging
from typing import Dict, List, Set


from python.entity import Entity, Wall, Player, DynamicEntity, SmallDot, Interactable
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

    def add_player(self, player: Player, coord: Coordinate):
        self._world.place_dynamic_entity(player, coord)
        self._player = player

    def add_dynamic_entity(self, entity: Entity, coord: Coordinate):
        self._world.place_dynamic_entity(entity, coord)

    def _tick(self, input):
        # Get input from controller (cli)
        # Async??
        try:
            self._update_player_velocity(DIRECTION_BINDS[input])
        except KeyError:
            logger.warning(f"Unknown Direction Keybind: {input}")

        # All things move on this board first
        tmp_board: List[List[Set[Entity]]] = gen_empty_board(
            # TODO: Improve how this call works for generating a temp board :(
            Coordinate(len(self._world.board), len(self._world.board[0])),
            set().copy,
        )

        # Move all Entities
        self._move_entities(tmp_board)

        # Perform actions for entities on same spot
        self._interact_entities(tmp_board)

        # Update board
        self._update_world(tmp_board)

    def _move_entities(self, tmp_board: List[List[List[Entity]]]):
        for old_coords, ent in World.enumerate_board(self._world.board):
            logging.debug(f"Ent {ent}")
            new_coords = old_coords
            if isinstance(ent, DynamicEntity):

                # TODO: Add get_surroundings()
                new_coords = ent.gen_move(self._world.get_surroundings(old_coords))
                if not self._is_valid_move(new_coords):
                    logger.info(f"Can't move entity, to {new_coords}")
                    new_coords = old_coords
            tmp_board[new_coords.x][new_coords.y].add(ent)

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

    def _interact_entities(self, tmp_board: List[List[List[Entity]]]):
        for coords, entity_list in World.enumerate_board(tmp_board):
            class_dict: Dict[type, Set] = {}
            for entity in entity_list:
                class_dict.setdefault(entity.__class__, set())
                class_dict[entity.__class__].add(entity)

            if self._dict_has(class_dict, Interactable) and self._dict_has(
                class_dict, Player
            ):
                interactable: Interactable
                for interactable in self._dict_get(class_dict, Interactable):
                    self._score += interactable.value

        # TODO: Add game logic for entity interactions

    def _update_world(self, tmp_board):
        for coords, entity_list in World.enumerate_board(tmp_board):
            for entity in entity_list:
                if isinstance(entity, DynamicEntity):
                    self._world.move_dynamic_entity(
                        entity, Coordinate(coords.x, coords.y)
                    )
