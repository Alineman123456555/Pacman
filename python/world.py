from typing import List, Tuple, Set
from python.coordinate import Coordinate

from python.entity import Entity, DynamicEntity, Wall

EMPTY_2X2_BOARD = [[None] * 2] * 2
EMPTY_4X4_BOARD = [[None] * 4] * 4
EMPTY_5X5_BOARD = [[None] * 5] * 5


def gen_empty_board(size: Coordinate, default_entity: Entity = None):
    return [[default_entity] * size.y for _ in range(size.x)]


class World:
    def __init__(self, size: Coordinate):
        """
        Bottom left is the start of the board.
        """
        self.board: List[List[Entity]] = gen_empty_board(size)
        self.dynamic_entities: Set[DynamicEntity] = set()

    def get_surroundings(self, coord: Coordinate):
        # TODO: Implement
        return NotImplemented

    def get_entity(self, coord: Coordinate):
        return self.board[coord.x][coord.y]

    def place_entity(self, entity: DynamicEntity, coord: Coordinate):
        self.board[coord.x][coord.y] = entity
        entity.coords = coord
        self.dynamic_entities.add(entity)

    def remove_entity(self, coord: Coordinate):
        self.board[coord.x][coord.y] = None

    def move_entity(self, entity: DynamicEntity, new_coords: Coordinate):
        self.remove_entity(entity.coords)
        self.place_entity(entity, new_coords)
