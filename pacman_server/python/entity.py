import logging

from abc import ABC, abstractmethod
from typing import Set, Tuple, Dict

from python.coordinate import Coordinate
from python.direction import Direction

logger = logging.getLogger(__name__)


class Entity(ABC):
    pass


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


class DynamicEntity(Entity):
    def __init__(self, coord: Coordinate = None, direction: Direction = Direction.NONE):
        self.coords: Coordinate = coord
        self.direction: Direction = direction
        self._last_tick: int = 0
        self.old_coords: Coordinate = coord

    @abstractmethod
    def gen_move(self, surroundings: Dict[Direction, "Cell"]) -> Coordinate:
        """Generates a move

        Parameters
        ----------
        A tuple (length 4 for directions), each index is a List[Entity]

        Returns
        -------
        Tuple[int, int]
            An x, y coordinate in the world.
        """
        # TODO: Refactor surroundings tuple to use a world singleton
        return NotImplementedError

    def update_coords(self, new_coords: Coordinate):
        self.old_coords = self.coords
        self.coords = new_coords


class Player(DynamicEntity):
    def __init__(self, coords: Coordinate = None):
        return super().__init__(coords)

    # TODO: Decide if getters and setters
    #   Makes it easier to avoid AttributeErrors
    # Maybe I should just init entities at (0, 0)
    # or just add a coord to the init

    def gen_move(self, surroundings: Dict[Direction, "Cell"]) -> Coordinate:
        # TODO: Figure out if you need to use surroundsing to generate the move.
        return self.coords + self.direction.value


class EatModePlayer(Player):
    def __init__(self, num_ticks: int, coords: Coordinate = None):
        """This class is a player, but interacts differently with Ghosts.
        Parameters
        ----------
        num_ticks: int
            The number of ticks this player should exist.
            Every gen_move() this is decremented
        """
        self._num_ticks = num_ticks
        super().__init__(coords)

    def gen_move(
        self,
        surroundings: Tuple[
            Entity,
            Entity,
            Entity,
            Entity,
        ],
    ) -> Coordinate:
        self._num_ticks -= 1
        logger.debug(f"EatModePlayer num_ticks remaining: {self._num_ticks}")
        return super().gen_move(surroundings)


class Ghost(DynamicEntity):
    def __init__(self, coord: Coordinate = None, direction: Direction = Direction.UP):
        super().__init__(coord, direction)

    pass


class DumbGhost(Ghost):
    def gen_move(self, surroundings: Dict[Direction, "Cell"]) -> Coordinate:
        # TODO: make logic check all 4 direction no matter what the starting direction is.
        # TODO: Fix formatting probably refactor this check to a function.
        if self.direction == Direction.RIGHT and surroundings[
            Direction.RIGHT
        ].has_class(Wall):
            self.direction = Direction.DOWN
        if self.direction == Direction.DOWN and surroundings[Direction.DOWN].has_class(
            Wall
        ):
            self.direction = Direction.LEFT
        if self.direction == Direction.LEFT and surroundings[Direction.LEFT].has_class(
            Wall
        ):
            self.direction = Direction.UP
        if self.direction == Direction.UP and surroundings[Direction.UP].has_class(
            Wall
        ):
            self.direction = Direction.RIGHT

        return self.coords + self.direction.value


class StaticEntity(Entity):
    pass


class Wall(StaticEntity):
    def __init__(self):
        # TODO: Figure out if something needs to be here
        pass


class Interactable(StaticEntity):
    @property
    @abstractmethod
    def value(self):
        """The score value of the interactible"""
        raise NotImplementedError


class SmallDot(Interactable):
    @property
    def value(self):
        return 100


class Fruit(Interactable):
    @property
    def value(self):
        raise NotImplementedError


class Cherry(Fruit):
    @property
    def value(self):
        return 100


class Strawberry(Fruit):
    @property
    def value(self):
        return 300


class Orange(Fruit):
    @property
    def value(self):
        return 500


class Apple(Fruit):
    @property
    def value(self):
        return 700


class Spawner(StaticEntity):
    # TODO: Need to think more about handing how things spawn.
    def __init__(self):
        raise NotImplementedError


class GhostSpawner(Spawner):
    # TODO: Decide if this should be an entity or stored seperately
    #   In the world class.
    def __init__(self):
        raise NotImplementedError


class FruitSpawner(Spawner):
    # TODO: Implement
    def __init__(self) -> None:
        raise NotImplementedError
