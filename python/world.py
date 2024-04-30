import logging
from typing import List, Tuple, Set, Callable, Generator, Dict, Iterable
from python.coordinate import Coordinate

from python.entity import Entity, DynamicEntity, Wall, Player
from python.direction import Direction

logger = logging.getLogger(__name__)


class Cell:
    """Stores entities at each spot in the worlds 2d array

    The entities are stored in a dictionary that maps
    Class type to a set of entities that are that type.
    This makes it easier to grab specific sets of entities in a
    Cell when doing various interactions.
    """

    def __init__(self):
        self._entity_dict: Dict[type, Set[Entity]] = {}

    def add_entity(self, entity: Entity) -> "Cell":
        self._entity_dict.setdefault(entity.__class__, set())
        self._entity_dict[entity.__class__].add(entity)
        return self

    def remove_entity(self, entity: Entity) -> "Cell":
        try:
            entity_set = self._entity_dict[entity.__class__]
            entity_set.remove(entity)
            if len(entity_set) == 0:
                logger.debug(f"Empty entity_set removing class: {entity.__class__}")
                self._entity_dict.pop(entity.__class__)
        except KeyError:
            # TODO: Don't know if this error should actually be returned
            logger.error(
                f"Tried deleting an entity that was not in this cell entity: {entity}"
                f"_entity_dict: {self._entity_dict}"
            )
        return self

    def get_all(self) -> Set[Entity]:
        all_ents = set()
        for ents in self._entity_dict.values():
            all_ents.update(ents)
        return all_ents

    def is_empty(self) -> bool:
        if self._entity_dict:
            return False
        return True

    def has_class(self, class_type: type) -> bool:
        if class_type in self._entity_dict.keys():
            return True
        return False

    def has_subclass(self, class_type: type) -> bool:
        for entity_class in self._entity_dict.keys():
            if issubclass(entity_class, class_type):
                return True
        return False

    def get_class_set(self, class_type: type) -> Set[Entity]:
        """Gets set of all entities that match class"""
        try:
            return self._entity_dict[class_type]
        except KeyError:
            # TODO: Don't know if this error should actually be returned
            logger.error(f"No class_type: {class_type}, " f"stored in Cell: {self}")
            return set()

    def get_subclass_set(self, class_type: type) -> Set[Entity]:
        """Gets set of all entities and children type"""
        full_entity_set = set()
        for entity_class, entity_set in self._entity_dict.items():
            if issubclass(entity_class, class_type):
                full_entity_set.update(entity_set)
        return full_entity_set


class World:
    """This class could actually be called Board. That's basically what it is
    A 2d board that has operations to help you place and move things.
    """

    def __init__(self, size: Coordinate = Coordinate(1, 1)):
        """
        Bottom left is the start of the board.
        """
        self.board: List[List[Cell]] = World.gen_empty_board(size)

    def get_surroundings(self, coord: Coordinate) -> Dict[Direction, Cell]:
        """Returns cells at RIGHT, LEFT, UP, DOWN"""
        return {
            Direction.RIGHT: self.get_cell(coord + Direction.RIGHT.value),
            Direction.LEFT: self.get_cell(coord + Direction.LEFT.value),
            Direction.UP: self.get_cell(coord + Direction.UP.value),
            Direction.DOWN: self.get_cell(coord + Direction.DOWN.value),
        }

    def get_cell(self, coord: Coordinate) -> Cell:
        # TODO: Figure out if you really need this.
        return self.board[coord.x][coord.y]

    def add_entity(self, entity: Entity, coord: Coordinate):
        # TODO: Figure out if you really need this
        self.board[coord.x][coord.y].add_entity(entity)

    def place_dynamic_entity(self, entity: DynamicEntity, coord: Coordinate):
        # TODO: Maybe remove the coord stuff
        #   But I feel this is a nice optimization b/c DynamicEntities
        #   Are touched frequently
        #   Could also have this take a generic entity and try to set the coords.
        #   and handle the attribute error.
        self.add_entity(entity, coord)
        entity.coords = coord

    def remove_dynamic_entity(self, entity: DynamicEntity):
        # TODO: Maybe remove the coord stuff
        coord = entity.coords
        self.board[coord.x][coord.y].remove_entity(entity)

    def move_dynamic_entity(self, entity: DynamicEntity, new_coords: Coordinate):
        logger.debug(f"Moving entity to coords: {new_coords}")
        self.remove_dynamic_entity(entity)
        self.place_dynamic_entity(entity, new_coords)

    def find_player(self) -> Player:
        """Finds the first player in the board"""
        for _, entity_list in World.enumerate(self.board):
            for entity in entity_list:
                if isinstance(entity, Player):
                    return entity

    def enumerate(self) -> Generator[Tuple[Coordinate, Cell], None, None]:
        for x, row in enumerate(self.board):
            for y, cell in enumerate(row):
                # for entity in entity_set:
                if not cell.is_empty():
                    yield (Coordinate(x, y), cell)

    @classmethod
    def gen_empty_board(cls, size: Coordinate) -> List[List[Cell]]:
        # TODO: Refactor so this is cleaner :(
        #   I don't like how the default_entity is created
        #   Maybe call it a default_entity generator? (factory???)
        #
        if size.x < 1 or size.y < 1:
            raise ValueError(
                f"gen_empty_board size must be greater than 0, size {size}"
            )
        return [[Cell() for _ in range(size.y)] for _ in range(size.x)]
