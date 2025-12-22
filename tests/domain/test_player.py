import pytest
from casino_lab4.domain.player import Player

def test_player_init():
    player = Player('John', 100)
    assert player.name == 'John'
    assert player.balance == 100
    assert player.sanity == 100
    assert player.alive == True

def test_player_init_with_sanity():
    player = Player('Jane', 200, sanity=50)
    assert player.name == 'Jane'
    assert player.balance == 200
    assert player.sanity == 50

def test_player_repr():
    player = Player('John', 100, sanity=80)
    assert repr(player) == "Player(name=John, balance=100, sanity=80, alive=True)"

def test_player_str():
    player = Player('John', 100, sanity=80)
    assert str(player) == "Player(name=John, balance=100, sanity=80, alive=True)"

def test_player_eq():
    player1 = Player('John', 100, sanity=80)
    player2 = Player('John', 100, sanity=80)
    player3 = Player('Jane', 100, sanity=80)
    
    assert player1 == player2
    assert player1 != player3
    assert player1 != "not a player"

def test_player_apply_sanity():
    player = Player('John', 100)
    
    player.apply_sanity(50)
    assert player.sanity == 50
    
    player.apply_sanity(120)
    assert player.sanity == 100
    
    player.apply_sanity(-10)
    assert player.sanity == 0

def test_player_rest():
    player = Player('John', 100, sanity=20)
    player.rest()
    assert player.sanity == 100

def test_player_can_act():
    player = Player('John', 100, sanity=50)
    assert player.can_act() == True
    
    player.apply_sanity(0)
    assert player.can_act() == False
    
    player.rest()
    player.die()
    assert player.can_act() == False

def test_player_die():
    player = Player('John', 100, sanity=50)
    player.die()
    assert player.alive == False
    assert player.sanity == 100

