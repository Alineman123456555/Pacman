import pytest

from python.entity import Interactable, SmallDot


def test_Interactable():
    with pytest.raises(TypeError):
        Interactable()


def test_SmallDot():
    assert SmallDot().value == 100
