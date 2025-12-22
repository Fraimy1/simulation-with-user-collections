import pytest
from casino_lab4.simulation.runner import run_simulation, _is_simulation_over
from casino_lab4.simulation.casino import Casino
from casino_lab4.domain.player import Player

def test_is_simulation_over_bankrupt():
    casino = Casino(bankroll=10000)
    casino.is_bankrupt = True
    
    is_over, reason = _is_simulation_over(casino)
    assert is_over == True
    assert "bankrupt" in reason.lower()

def test_is_simulation_over_no_money():
    casino = Casino(bankroll=0)
    
    is_over, reason = _is_simulation_over(casino)
    assert is_over == True
    assert "money" in reason.lower()

def test_is_simulation_over_all_dead():
    casino = Casino(bankroll=10000)
    player1 = Player('John', 100)
    player2 = Player('Jane', 200)
    player1.die()
    player2.die()
    casino.register_player(player1)
    casino.register_player(player2)
    
    is_over, reason = _is_simulation_over(casino)
    assert is_over == True
    assert "dead" in reason.lower()

def test_is_simulation_over_all_broke():
    casino = Casino(bankroll=10000)
    player1 = Player('John', 0)
    player2 = Player('Jane', 0)
    casino.register_player(player1)
    casino.register_player(player2)
    
    is_over, reason = _is_simulation_over(casino)
    assert is_over == True
    assert "broke" in reason.lower()

def test_is_simulation_not_over():
    casino = Casino(bankroll=10000)
    player = Player('John', 100)
    casino.register_player(player)
    
    is_over, reason = _is_simulation_over(casino)
    assert is_over == False
    assert reason == ""

def test_run_simulation():
    run_simulation(steps=5, seed=42)

def test_run_simulation_ends_early_bankrupt():
    casino = Casino(bankroll=10)
    player = Player('John', 0)
    casino.register_player(player)
    
    is_over, reason = _is_simulation_over(casino)
    assert is_over == True

def test_run_simulation_long():
    run_simulation(steps=100, seed=123)

