from __future__ import annotations
from typing import Iterator
from loguru import logger
from casino_lab4.utils.logging import log_and_raise
from casino_lab4.core.errors import NotFoundError, OutOfRangeError, WrongTypeError, StepZeroError
from casino_lab4.domain.player import Player

class PlayerCollection:
    def __init__(self, data: list[Player] | None = None) -> None:
        self._data: list[Player] = data.copy() if data is not None else []
    
    def __len__(self) -> int:
        return len(self._data)

    def __setitem__(self, i: int, player: Player) -> None:
        if not isinstance(i, int):
            log_and_raise(WrongTypeError("Index must be an integer"))
        
        try:
            self._data[i] = player
        except IndexError:
            log_and_raise(OutOfRangeError(f"Player at index {i} not found"))

        logger.info(f"Player number {i} changed: {player}")

    def __getitem__(self, i: int|slice) -> Player|PlayerCollection:
        if not isinstance(i, (int,slice)):
            log_and_raise(WrongTypeError("Index must be an integer or a slice"))
        
        if isinstance(i, slice):
            if i.step is not None and i.step == 0:
                log_and_raise(StepZeroError("Step must be non-zero"))
            
            return PlayerCollection(self._data[i])
        else:
            try:
                return self._data[i]
            except IndexError:
                log_and_raise(OutOfRangeError(f"Player at index {i} not found"))
        
        raise NotImplementedError("Index must be an integer or a slice")

    def __iter__(self) -> Iterator[Player]:
        return iter(self._data)

    def __delitem__(self, i: int) -> None:
        if not isinstance(i, int):
            log_and_raise(WrongTypeError("Index must be an integer"))
        
        try:
            self._data.pop(i)
        except IndexError:
            log_and_raise(OutOfRangeError(f"Player at index {i} not found"))
        
        logger.info(f"Player number {i} deleted")

    def remove(self, player: Player) -> None:
        if not isinstance(player, Player):
            log_and_raise(WrongTypeError("Player must be a Player object"))
        
        for i, p in enumerate(self._data):
            if p.name == player.name:
                del self[i]
                return
        log_and_raise(NotFoundError(f"Player {player.name} not found"))
        logger.info(f"Player {player.name} deleted")
    
    def append(self, player: Player) -> None:
        if not isinstance(player, Player):
            log_and_raise(WrongTypeError("Player must be a Player object"))
        
        self._data.append(player)
        logger.info(f"Player appended: {player}")

    def __repr__(self) -> str:
        return f"PlayerCollection({self._data})"