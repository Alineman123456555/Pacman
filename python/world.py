import logging
from typing import List, Tuple, Set, Callable, Generator, Dict
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

    def add_entity(self, entity: Entity):
        self._entity_dict.setdefault(entity.__class__, set())
        self._entity_dict[entity.__class__].add(entity)

    def remove_entity(self, entity: Entity) -> None:
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
        self.board: List[List[Set[Entity]]] = World.gen_empty_board(size)

    def get_surroundings(self, coord: Coordinate):
        """Returns entities at RIGHT, LEFT, UP, DOWN"""
        return (
            self.get_entities(coord + Direction.RIGHT.value),
            self.get_entities(coord + Direction.LEFT.value),
            self.get_entities(coord + Direction.UP.value),
            self.get_entities(coord + Direction.DOWN.value),
        )

    def get_entities(self, coord: Coordinate) -> Set[Entity]:
        return self.board[coord.x][coord.y]

    def place_dynamic_entity(self, entity: DynamicEntity, coord: Coordinate):
        self.board[coord.x][coord.y].add(entity)
        entity.coords = coord

    def remove_entity(self, entity: DynamicEntity):
        coord = entity.coords
        self.board[coord.x][coord.y].remove(entity)

    def move_dynamic_entity(self, entity: DynamicEntity, new_coords: Coordinate):
        logger.debug(f"Moving entity to coords: {new_coords}")
        self.remove_entity(entity)
        self.place_dynamic_entity(entity, new_coords)

    def find_player(self) -> Player:
        """Finds the first player in the board"""
        for _, entity_list in World.enumerate_board(self.board):
            for entity in entity_list:
                if isinstance(entity, Player):
                    return entity

    @classmethod
    def gen_empty_board(
        cls, size: Coordinate, default_entity: Callable[[], Entity] = lambda: []
    ):
        # TODO: Refactor so this is cleaner :(
        #   I don't like how the default_entity is created
        #   Maybe call it a default_entity generator? (factory???)
        #
        if size.x < 1 or size.y < 1:
            raise ValueError(
                f"gen_empty_board size must be greater than 0, size {size}"
            )
        return [[set(default_entity()) for _ in range(size.y)] for _ in range(size.x)]

    @classmethod
    def enumerate_board(
        cls, board: List[List[Set[Entity]]]
    ) -> Generator[Tuple[Coordinate, Set[Entity]], None, None]:
        for x, row in enumerate(board):
            for y, entity_set in enumerate(row):
                # for entity in entity_set:
                if entity_set:
                    yield (Coordinate(x, y), entity_set)
