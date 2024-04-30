import pytest

from python.coordinate import Coordinate
from python.world import World, Cell
from python.entity import Player, Entity, DumbGhost, Wall, Ghost


def test_World_gen_empty_board():
    with pytest.raises(ValueError):
        World.gen_empty_board(Coordinate(0, 0))

    board = World.gen_empty_board(Coordinate(2, 1))
    assert len(board) == 2
    assert len(board[0]) == 1
    assert isinstance(board[0][0], Cell)
    assert board[0][0].is_empty()


def test_World__init__():
    world = World(Coordinate(1, 1))
    assert world.board
    assert world.board[0][0].is_empty()


def test_World_add_entity():
    world = World(Coordinate(2, 1))
    world.add_entity(Wall(), Coordinate(0, 0))
    assert not world.board[0][0].is_empty()
    assert world.board[1][0].is_empty()


def test_World_get_cell():
    world = World(Coordinate(2, 1))
    wall = Wall()
    world.add_entity(wall, Coordinate(0, 0))
    assert not world.get_cell(Coordinate(0, 0)).is_empty()
    assert world.get_cell(Coordinate(1, 0)).is_empty()


def test_World_place_dynamic_entity():
    player = Player()
    world = World(Coordinate(1, 1))

    world.place_dynamic_entity(player, Coordinate(0, 0))
    assert player.coords == Coordinate(0, 0)


def test_enumerate():
    world = World(Coordinate(3, 1))

    cell = Cell()
    cell.add_entity(Wall())
    cell.add_entity(Player())
    cell_2 = Cell()
    cell_2.add_entity(DumbGhost())

    world.board[0][0] = cell
    world.board[2][0] = cell_2

    cells = list(world.enumerate())
    assert len(cells) == 2  # Empty cells aren't returned

    assert cells[0][0] == Coordinate(0, 0)
    assert cells[0][1].has_class(Wall)
    assert cells[0][1].has_class(Player)

    assert cells[1][0] == Coordinate(2, 0)
    assert cells[1][1].has_class(DumbGhost)


def test_Cell_init():
    cell = Cell()
    assert not cell._entity_dict


def test_Cell_add_entity():
    cell = Cell()
    wall = Wall()
    cell.add_entity(wall)
    assert cell._entity_dict
    assert cell._entity_dict[Wall] == {wall}


def test_Cell_is_empty():
    cell = Cell()
    assert cell.is_empty()
    cell.add_entity(Wall())
    assert not cell.is_empty()


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


def test_Cell_get_all():
    cell = Cell()
    player = Player()
    wall = Wall()
    cell.add_entity(player)
    cell.add_entity(wall)

    for ent in cell.get_all():
        assert ent in {player, wall}
