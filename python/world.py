import logging
from typing import List, Tuple, Set, Callable, Generator, Dict
from python.coordinate import Coordinate

from python.entity import Entity, DynamicEntity, Wall, Player
from python.direction import Direction

logger = logging.getLogger(__name__)


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
