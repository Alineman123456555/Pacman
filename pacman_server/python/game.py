import logging

from typing import Dict, List, Set

from python.entity import (
    Entity,
    Wall,
    Player,
    DynamicEntity,
    Interactable,
    Ghost,
    Cell,
    SmallDot,
    DumbGhost,
    EatModePlayer,
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

ENTITY_TO_CHAR: Dict[Entity, str] = {
    type(None): ".",
    Wall: "X",
    Player: "O",
    SmallDot: "-",
    DumbGhost: "G",
    EatModePlayer: "0",
}

CHAR_PRIORITY: Dict[str, int] = {
    ".": 0,
    "X": 1000,
    "O": 99,
    "-": 50,
    "G": 60,
    "0": 100,
}

CHAR_TO_ENTITY: Dict[str, Entity] = {
    ".": type(None),
    "X": Wall,
    "O": Player,
    "-": SmallDot,
    "G": DumbGhost,
    "0": EatModePlayer,
}


class Game:
    # TODO: Rename to PacmanGame
    #   Move generic class functions to an abstract class Game
    def __init__(self, world: World = World(Coordinate(1, 1))) -> None:
        self._world = world
        self._score = 0
        self._player = None
        self._tick_count = 0

    def load_game(self):
        # Build World
        self._world.board = self._load_board(config.WORLD_FILE)

        # Create Game
        self._player = self._world.find_player()

        return self

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
        self._move_entities()
        # TODO: Right movement and up movement for the player now teleports
        #   the players as far as possible.
        # TODO: When ghost moves up he teleports up and right
        #   then moves down one.
        #   THIS ALL STARTED HAPPENING AFTER REMOVING THE TEMP WORLD.
        self._tick_count += 1

        # Perform actions for entities on same spot
        self._interact_entities()

        # Check if game is over
        # TODO: Refactor
        if not self._player:
            logger.error("No player!")
            # TODO: Add respawn
            return 1
        return 0

    def _move_entities(self):
        for old_coords, cell in self._world.enumerate():
            dyent: DynamicEntity
            for dyent in cell.get_subclass_set(DynamicEntity):
                logger.info(f"Moving dyent, coords: {old_coords}")
                if dyent._last_tick < self._tick_count:
                    new_coords = dyent.gen_move(
                        self._world.get_surroundings(old_coords)
                    )
                    if not self._is_valid_move(new_coords):
                        logger.info(f"Can't move entity, to {new_coords}")
                        new_coords = old_coords
                    self._world.move_dynamic_entity(dyent, new_coords)
                    dyent._last_tick = self._tick_count

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

    def __check_current_and_old(self, dyent: DynamicEntity, class_type: type):
        # TODO: Move to world.py
        #   Is this too much logic for the world?
        return self._world.get_cell(dyent.coords).has_subclass(
            class_type
        ) or self._world.get_cell(dyent.old_coords).has_subclass(class_type)

    def __player_interactions(self, cell: Cell):
        player: Player
        for player in cell.get_subclass_set(Player):
            logger.info(f"Found player for interactions")

            # Player, Interactable interaction
            interactable: Interactable
            for interactable in cell.get_subclass_set(Interactable):
                logger.info(f"Player, Interactable interaction")
                self._score += interactable.value
                cell.remove_entity(interactable)
                # TODO: Make it so an interactable can do other things in the tick
                #    Before being removed? Basically add it to a set of entities
                #    that get removed at the end of _interact_entities
                # Player, Ghost interaction
                # TODO: Refactor player/ghost interaction

            if self.__check_current_and_old(player, Ghost):
                # TODO: Change it so the player can actually
                #   escape from a ghost. So don't check the old spot.
                #   Or check the old spot and then check if the ghost and
                #   have specifically switched spots.
                # TODO: Refactor this and below
                logger.info(f"Player, Ghost interaction")
                self._player = None
                self._world.remove_dynamic_entity(player)

    def __ghost_interactions(self, cell: Cell):
        ghost: Ghost
        for ghost in cell.get_subclass_set(Ghost):
            if self.__check_current_and_old(ghost, Player):
                # TODO: Refactor.
                logger.info(f"Player, Ghost interaction")
                self._player = None
                # TODO: get rid of this for loop. Somehow it can be moved out of this :(
                for player in cell.get_subclass_set(Player):
                    self._world.remove_dynamic_entity(player)

    def _interact_entities(self):
        for coords, cell in self._world.enumerate():
            pass
            self.__player_interactions(cell)

            self.__ghost_interactions(cell)

        # TODO: Add game logic for entity interactions

    @classmethod
    def __entity_to_char(cls, ent: Entity):
        # TODO: Move to a new class PacmanWorld
        #   This new class just adds a few functions for rendering the game
        #   that are unique to pacman.
        return ENTITY_TO_CHAR[ent.__class__]

    def _world_to_string(self) -> str:
        """It might make sense to move this to the World class
        But currently there's no good generic way to represent a world
        as a string. This game "pacman" has its own special way.
        That's why it is here.
        """
        # TODO: Maybe add to a layer between game and api?
        # TODO: Probably move to World class
        # Yeah it would be nice for testing? Wait no?
        board = self._world.board

        y_str_list = [""] * len(board[0])
        logger.debug(f"board: {board}")
        for column in board:
            logger.debug(f"column: {column}")
            for yidx, cell in enumerate(reversed(column)):
                # TODO: Refactor this 3rd loop. Something about how this renders overlaps I don't like
                char = Game.__entity_to_char(None)
                logger.debug(f"Cell: {cell}")
                for ent in cell.get_all():
                    temp = Game.__entity_to_char(ent)
                    if CHAR_PRIORITY[temp] > CHAR_PRIORITY[char]:
                        # TODO: Improve how priority is stored/calculated
                        #   can probably just use the ENTITY_TO_CHAR dict for this.
                        #   order is deterministic so the order of ENTITY_TO_CHAR
                        #   can determine the priority
                        char = temp

                y_str_list[yidx] += char

        return "\n".join(y_str_list) + "\n"

    def _load_board(self, filename: str) -> List[List[Cell]]:
        # TODO: Move to PacmanWorld
        # TODO: Probably should have this function return a world.
        #   Board and world have sorta been used interchangably throughout
        #   this project.
        board_str = ""
        with open(filename, "r") as f:
            board_str = f.read().strip()

        row_list = board_str.split("\n")
        y_size = len(row_list)
        x_size = len(row_list[0])

        board = World.gen_empty_board(Coordinate(x_size, y_size))
        logger.debug(f"Empty board size x: {len(board)}, y: {len(board[0])}")
        for yidx, row in enumerate(reversed(row_list)):
            logger.debug(f"Row: '{row}', len: {len(row)}")
            for xidx, char in enumerate(row):
                logger.debug(f"Loading char: {char}, xidx: {xidx}, yidx: {yidx}")
                entity = CHAR_TO_ENTITY[char]()
                if entity:  # TODO: I don't like this. idk.
                    if isinstance(entity, DynamicEntity):
                        entity.coords = Coordinate(xidx, yidx)
                        entity.old_coords = Coordinate(xidx, yidx)
                    board[xidx][yidx].add_entity(entity)

        return board
