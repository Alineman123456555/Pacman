import pytest

from python.coordinate import Coordinate
from python.world import World, Cell
from python.entity import Player, Entity, DumbGhost, Wall, Ghost


def test_World_gen_empty_board():
    with pytest.raises(ValueError):
        World.gen_empty_board(Coordinate(0, 0))

    assert World.gen_empty_board(Coordinate(2, 1)) == [[set()], [set()]]


def test_World__init__():
    # TODO: Make better?
    world = World(Coordinate(2, 2))
    assert world.board == [[set(), set()], [set(), set()]]


def test_World_move_entity():
    world = World(Coordinate(2, 2))
    assert False


def test_World_place_dynamic_entity():
    player = Player()
    world = World(Coordinate(3, 3))

    world.place_dynamic_entity(player, Coordinate(1, 1))
    assert world.board == [
        [set(), set(), set()],
        [set(), {player}, set()],
        [set(), set(), set()],
    ]


def test_Cell_init():
    cell = Cell()
    assert cell._entity_dict is None


def test_Cell_add_entity():
    cell = Cell()
    wall = Wall()
    cell.add_entity(wall)
    assert cell._entity_dict
    assert cell._entity_dict[Wall] == {wall}


def test_Cell_remove_entity():
    cell = Cell()
    wall = Wall()
    wall_2 = Wall()

    # Removes only one
    cell.add_entity(wall)
    cell.add_entity(wall_2)
    cell.remove_entity(wall_2)
    assert cell._entity_dict[Wall] == {wall}

    # Removes from the whole dict
    cell.remove_entity(wall)
    assert not cell._entity_dict


@pytest.fixture
def monkey_Ghost(monkeypatch):
    monkeypatch.setattr(Ghost, "__abstractmethods__", set())


def test_Cell_has_class(monkey_Ghost):
    cell = Cell()
    cell.add_entity(Ghost())

    assert cell.has_class(Ghost)
    assert cell.has_class(Entity) is False
    assert cell.has_class(Player) is False
    assert cell.has_class(DumbGhost) is False


def test_Cell_has_subclass(monkey_Ghost):
    cell = Cell()
    cell.add_entity(Ghost())

    assert cell.has_subclass(Ghost)
    assert cell.has_subclass(Entity)
    assert cell.has_subclass(Player) is False
    assert cell.has_subclass(DumbGhost) is False


def test_Cell_get_class_set(monkey_Ghost):
    cell = Cell()
    ghost = Ghost()
    cell.add_entity(ghost)

    assert cell.get_class_set(Ghost) == {ghost}
    assert not cell.get_class_set(Entity)
    assert not cell.get_class_set(Player)
    assert not cell.get_class_set(DumbGhost)


def test_Cell_get_subclass_set(monkey_Ghost):
    cell = Cell()
    ghost = Ghost()
    cell.add_entity(ghost)

    assert cell.get_subclass_set(Ghost) == {ghost}
    assert cell.get_subclass_set(Entity) == {ghost}
    assert not cell.get_subclass_set(Player)
    assert not cell.get_subclass_set(DumbGhost)
