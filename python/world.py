import logging

from typing import List, Tuple, Callable, Generator, Dict, Iterable

from python.coordinate import Coordinate
from python.entity import Entity, DynamicEntity, Wall, Player, Cell
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
        self.board: List[List[Cell]] = World.gen_empty_board(size)

    @property
    def size(self):
        return Coordinate(len(self.board), len(self.board[0]))

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
        entity.update_coords(coord)

    def remove_dynamic_entity(self, entity: DynamicEntity):
        # TODO: Maybe remove the coord stuff
        coord = entity.coords
        self.board[coord.x][coord.y].remove_entity(entity)

    def move_dynamic_entity(self, entity: DynamicEntity, new_coords: Coordinate):
        # TODO: I think a lot of this code is not necessary.
        logger.debug(f"Moving entity to coords: {new_coords}")
        self.remove_dynamic_entity(entity)
        self.place_dynamic_entity(entity, new_coords)

    def find_player(self) -> Player:
        """Finds the first player in the board"""
        for _, cell in self.enumerate():
            if cell.has_class(Player):
                # TODO: Make find all players
                return list(cell.get_class_set(Player))[0]

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
