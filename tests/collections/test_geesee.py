from casino_lab4.collections.geese import GooseCollection
import pytest
from casino_lab4.core.errors import (
    NotFoundError,
    OutOfRangeError,
    WrongTypeError,
    StepZeroError,
)
from casino_lab4.domain.goose import Goose


@pytest.fixture
def geese() -> GooseCollection:
    gc = GooseCollection()
    gc.append(Goose("Gus", 100))
    gc.append(Goose("Lily", 200))
    gc.append(Goose("Daisy", 300))
    return gc


def test_len(geese):
    assert len(geese) == 3
    geese[0] = Goose("Honker", 200)
    assert geese[0].name == "Honker"
    assert geese[0].honk_volume == 200


def test_get_slice(geese):
    sub = geese[0:2]
    assert isinstance(sub, GooseCollection)
    assert [g.name for g in sub] == ["Gus", "Lily"]
    assert [g.honk_volume for g in sub] == [100, 200]

    rev = geese[::-1]
    assert [g.name for g in rev] == ["Daisy", "Lily", "Gus"]

    stepped = geese[::2]
    assert [g.name for g in stepped] == ["Gus", "Daisy"]

    clamped = geese[0:999]
    assert [g.name for g in clamped] == ["Gus", "Lily", "Daisy"]

    sub[0] = Goose("ZZZ", 999)
    assert geese[0].name == "Gus"
    assert geese[0].honk_volume == 100


def test_errors_get(geese):
    with pytest.raises(OutOfRangeError):
        geese[10]

    with pytest.raises(WrongTypeError):
        geese["10"]

    with pytest.raises(StepZeroError):
        geese[0:2:0]


def test_errors_set(geese):
    with pytest.raises(WrongTypeError):
        geese["10"] = Goose("Honker", 200)

    with pytest.raises(OutOfRangeError):
        geese[10] = Goose("Honker", 200)


def test_iter(geese):
    assert [g.name for g in geese] == ["Gus", "Lily", "Daisy"]


def test_delete(geese):
    del geese[0]
    assert len(geese) == 2


def test_errors_delete(geese):
    with pytest.raises(WrongTypeError):
        del geese["1"]

    with pytest.raises(OutOfRangeError):
        del geese[10]


def test_errors_append(geese):
    with pytest.raises(WrongTypeError):
        geese.append("Honker")


def test_append(geese):
    geese.append(Goose("Honker", 200))
    assert len(geese) == 4
    assert geese[3].name == "Honker"
    assert geese[3].honk_volume == 200


def test_remove(geese):
    geese.remove(Goose("Gus", 100))
    assert len(geese) == 2


def test_errors_remove(geese):
    with pytest.raises(WrongTypeError):
        geese.remove("Gus")

    with pytest.raises(NotFoundError):
        geese.remove(Goose("azazaza", 200))


def test_repr(geese):
    result = repr(geese)
    assert "GooseCollection" in result
