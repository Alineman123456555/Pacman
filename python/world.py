from typing import List, Tuple

from python.entity import Entity, DynamicEntity, Wall

EMPTY_2X2_BOARD = [[None] * 2] * 2
EMPTY_4X4_BOARD = [[None] * 4] * 4


class World:
    def __init__(self):
        """
        Bottom left is the start of the board.
        """
        # TODO: Add board size as an input
        self.board: List[List[Entity]] = EMPTY_2X2_BOARD
        self.dynamic_entities: List[DynamicEntity] = []
        # TODO: Could refactor List[Entity] to be a WorldSpace Class?

    def get_surroundings(self, coord: Tuple[int, int]):
        # TODO: Implement
        return NotImplemented

    def place_entity():
        # TODO: Implement
        return NotImplemented

    def move_entity(self, entity: DynamicEntity, new_coords: Tuple[int, int]):
        old_coords = entity.coords
        entity.coords = new_coords
        self.board[new_coords[0], new_coords[1]]
