from casino_lab4.simulation.casino import Casino
from casino_lab4.domain.player import Player
from casino_lab4.domain.goose import Goose

def test_casino_init():
    casino = Casino(bankroll=10000)
    assert casino.bankroll == 10000
    assert len(casino.players) == 0
    assert len(casino.geese) == 0
    assert not casino.is_bankrupt

def test_casino_register_player():
    casino = Casino(bankroll=10000)
    player = Player('John', 100)
    casino.register_player(player)

    assert len(casino.players) == 1
    assert casino.balances['John'] == 100

def test_casino_register_goose():
    casino = Casino(bankroll=10000)
    goose = Goose('Gus', 50, balance=100)
    casino.register_goose(goose)

    assert len(casino.geese) == 1
    assert casino.geese_balances['Gus'] == 100

def test_casino_unregister_player():
    casino = Casino(bankroll=10000)
    player = Player('John', 100)
    casino.register_player(player)
    casino.unregister_player(player)

    assert len(casino.players) == 0
    assert 'John' not in casino.balances

def test_casino_unregister_goose():
    casino = Casino(bankroll=10000)
    goose = Goose('Gus', 50)
    casino.register_goose(goose)
    casino.unregister_goose(goose)

    assert len(casino.geese) == 0
    assert 'Gus' not in casino.geese_balances
