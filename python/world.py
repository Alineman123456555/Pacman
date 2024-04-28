import logging
from typing import List, Tuple, Set, Callable, Generator
from python.coordinate import Coordinate

from python.entity import Entity, DynamicEntity, Wall

logger = logging.getLogger(__name__)

EMPTY_2X2_BOARD = [[None] * 2] * 2
EMPTY_4X4_BOARD = [[None] * 4] * 4
EMPTY_5X5_BOARD = [[None] * 5] * 5


def gen_empty_board(
    size: Coordinate, default_entity: Callable[[], Entity] = lambda: None
):
    # TODO: Refactor so this is cleaner :(
    #   I don't like how the default_entity is created
    #   Maybe call it a default_entity generator? (factory???)
    return [[default_entity() for _ in range(size.y)] for _ in range(size.x)]


class World:
    def __init__(self, size: Coordinate):
        """
        Bottom left is the start of the board.
        """
        self.board: List[List[Entity]] = gen_empty_board(size)

        # TODO: Move dynamic_entities to game class

    def get_surroundings(self, coord: Coordinate):
        # TODO: Implement
        return NotImplemented

    def get_entity(self, coord: Coordinate):
        return self.board[coord.x][coord.y]

    def place_entity(self, entity: DynamicEntity, coord: Coordinate):
        self.board[coord.x][coord.y] = entity
        entity.coords = coord

    def remove_entity(self, coord: Coordinate):
        self.board[coord.x][coord.y] = None

    def move_entity(self, entity: DynamicEntity, new_coords: Coordinate):
        logger.debug(f"Moving entity to coords: {new_coords}")
        self.remove_entity(entity.coords)
        self.place_entity(entity, new_coords)

    @classmethod
    def enumerate_board(
        cls, board: List[List[Entity]]
    ) -> Generator[Tuple[Coordinate, Entity], None, None]:
        for x, row in enumerate(board):
            for y, entity in enumerate(row):
                if entity:
                    yield (Coordinate(x, y), entity)
