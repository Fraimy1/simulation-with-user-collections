from casino_lab4.collections.players import PlayerCollection
import pytest
from casino_lab4.core.errors import NotFoundError, OutOfRangeError, WrongTypeError, StepZeroError
from casino_lab4.domain.player import Player

@pytest.fixture
def players() -> PlayerCollection:
    pc = PlayerCollection()
    pc.append(Player("John", 100))
    pc.append(Player("Dan", 200))
    pc.append(Player("Lilly", 300))
    return pc

def test_len(players):
    assert len(players) == 3
    players[0] = Player("Jane", 200)
    assert players[0].name == "Jane"
    assert players[0].balance == 200

def test_get_slice(players):
    sub = players[0:2]
    assert isinstance(sub, PlayerCollection)
    assert [p.name for p in sub] == ["John", "Dan"]
    assert [p.balance for p in sub] == [100, 200]

    rev = players[::-1]
    assert [p.name for p in rev] == ["Lilly", "Dan", "John"]

    stepped = players[::2]
    assert [p.name for p in stepped] == ["John", "Lilly"]

    clamped = players[0:999]
    assert [p.name for p in clamped] == ["John", "Dan", "Lilly"]

    sub[0] = Player("ZZZ", 999)
    assert players[0].name == "John"
    assert players[0].balance == 100

def test_errors_get(players):
    with pytest.raises(OutOfRangeError):
        players[10]

    with pytest.raises(WrongTypeError):
        players["10"]

    with pytest.raises(StepZeroError):
        players[0:2:0]

def test_errors_set(players):
    with pytest.raises(WrongTypeError):
        players["10"] = Player("Jane", 200)

    with pytest.raises(OutOfRangeError):
        players[10] = Player("Jane", 200)

def test_iter(players):
    assert [p.name for p in players] == ["John", "Dan", "Lilly"]

def test_delete(players):
    del players[0]
    assert len(players) == 2

def test_remove(players):
    players.remove(Player("John", 100))
    assert len(players) == 2

def test_errors_remove(players):
    with pytest.raises(WrongTypeError):
        players.remove("John")
    with pytest.raises(NotFoundError):
        players.remove(Player("Honker", 200))

def test_errors_delete(players):
    with pytest.raises(WrongTypeError):
        del players["1"]

    with pytest.raises(OutOfRangeError):
        del players[10]

def test_errors_append(players):
    with pytest.raises(WrongTypeError):
        players.append("Jane")

def test_append(players):
    players.append(Player("Jane", 200))
    assert len(players) == 4
    assert players[3].name == "Jane"
    assert players[3].balance == 200

def test_repr(players):
    result = repr(players)
    assert "PlayerCollection" in result
