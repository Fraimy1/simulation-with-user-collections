from casino_lab4.collections.balances import CasinoBalance
import pytest
from casino_lab4.core.errors import NotFoundError

def test_casino_balance():
    balance = CasinoBalance()
    balance['John'] = 100
    assert balance['John'] == 100

    assert len(balance) == 1
    
    assert 'John' in balance
    assert 'Jane' not in balance
    
    with pytest.raises(NotFoundError):
        balance['Jane']
    
    balance['John'] = 200
    assert balance['John'] == 200

    del balance['John']
    assert len(balance) == 0
    assert 'John' not in balance
    with pytest.raises(NotFoundError):
        balance['John']

    balance['Jane'] = 40

    balance.remove('Jane')
    assert len(balance) == 0

    with pytest.raises(NotFoundError):
        balance.remove('Jane')