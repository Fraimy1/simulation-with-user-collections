from typing import Iterator
from loguru import logger
from casino_lab4.utils.logging import log_and_raise
from casino_lab4.core.errors import NotFoundError
from casino_lab4.domain.player import Player

class PlayerCollection:
    def __init__(self) -> None:
        self._data: list[Player] = []
    
    def __len__(self) -> int:
        return len(self._data)

    def __setitem__(self, i: int, player: Player) -> None:
        if i not in range(len(self._data)):
            log_and_raise(NotFoundError(f"Player at index {i} not found"))
        
        self._data[i] = player
        logger.info(f"Player number {i} changed: {player}")

    def __getitem__(self, i: int) -> Player:
        if i not in range(len(self._data)):
            log_and_raise(NotFoundError(f"Player at index {i} not found"))
        
        return self._data[i]
    
    def __iter__(self) -> Iterator[Player]:
        return iter(self._data)

    def __delitem__(self, i: int) -> None:
        player = self._data.pop(i)
        if player is None:
            log_and_raise(NotFoundError(f"Player at index {i} not found"))
        
        logger.info(f"Player number {i} deleted: {player}")

    def append(self, player: Player) -> None:
        self._data.append(player)
        logger.info(f"Player appended: {player}")