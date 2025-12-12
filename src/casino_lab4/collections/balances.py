from typing import Iterator
from loguru import logger
from casino_lab4.utils.logging import log_and_raise
from casino_lab4.core.errors import NotFoundError

class CasinoBalance:
    def __init__(self) -> None:
        self._balances: dict[str : float] = {}
    
    def __len__(self) -> int:
        return len(self._balances)

    def __setitem__(self, name: str, balance: float) -> None:
        old = self._balances.get(name)
        self._balances[name] = balance
        logger.info(f"Player balance changed: {old if old is not None else 'None'} -> {balance}")

    def __getitem__(self, name: str) -> float:
        balance = self._balances.get(name)
        if balance is None:
            log_and_raise(NotFoundError(f"Balance for player {name} not found"))
        
        return balance
    
    def __iter__(self) -> Iterator[str]:
        return iter(self._balances)

    def __delitem__(self, name: str) -> None:
        balance = self._balances.pop(name, None)
        if balance is None:
            log_and_raise(NotFoundError(f"Balance for player {name} not found"))
        
        logger.info(f"Player balance deleted: {name}")

    def remove(self, name: str) -> None:
        del self[name]
    
