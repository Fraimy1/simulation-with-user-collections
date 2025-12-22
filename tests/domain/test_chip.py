from casino_lab4.domain.chip import Chip
import pytest


def test_chip_add():
    assert (Chip(5) + Chip(7)).value == 12

    assert (Chip(5) + 7).value == 12

    with pytest.raises(TypeError):
        Chip(5) + 2.1

    assert (7 + Chip(5)).value == 12


def test_chip_repr():
    assert repr(Chip(12)) == "Chip(12)"
