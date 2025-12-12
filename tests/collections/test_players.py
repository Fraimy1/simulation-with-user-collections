from casino_lab4.collections.players import PlayerCollection
import pytest
from casino_lab4.core.errors import NotFoundError
from casino_lab4.domain.player import Player

def test_player_collection():
    players = PlayerCollection()
    players.append(Player('John', 100))
    players.append(Player('Dan', 200))
    
    with pytest.raises(NotFoundError):
        players[10]

    with pytest.raises(NotFoundError):
        players[10] = Player('Jane', 200)

    assert len(players) == 2

    players[0] = Player('Jane', 200)
    assert players[0].name == 'Jane'
    assert players[0].balance == 200

    assert [player.name for player in players] == ['Jane', 'Dan']

    del players[0]
    assert len(players) == 1

    with pytest.raises(NotFoundError):
        players[10]
        