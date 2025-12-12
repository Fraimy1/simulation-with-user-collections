from __future__ import annotations
from typing import Iterator
from loguru import logger
from casino_lab4.utils.logging import log_and_raise
from casino_lab4.core.errors import OutOfRangeError, WrongTypeError, StepZeroError
from casino_lab4.domain.goose import Goose
class GooseCollection:
    def __init__(self, data: list[Goose] | None = None) -> None:
        self._data: list[Goose] = data.copy() if data is not None else []
    
    def __len__(self) -> int:
        return len(self._data)

    def __setitem__(self, i: int, goose: Goose) -> None:
        if not isinstance(i, int):
            log_and_raise(WrongTypeError("Index must be an integer"))
        
        try:
            self._data[i] = goose
        except IndexError:
            log_and_raise(OutOfRangeError(f"Goose at index {i} not found"))

        logger.info(f"Goose number {i} changed: {goose}")

    def __getitem__(self, i: int|slice) -> Goose|GooseCollection:
        if not isinstance(i, (int,slice)):
            log_and_raise(WrongTypeError("Index must be an integer or a slice"))
        
        if isinstance(i, slice):
            if i.step is not None and i.step == 0:
                log_and_raise(StepZeroError("Step must be non-zero"))
            
            return GooseCollection(self._data[i])
        else:
            try:
                return self._data[i]
            except IndexError:
                log_and_raise(OutOfRangeError(f"Goose at index {i} not found"))
        
        raise NotImplementedError("Index must be an integer or a slice")

    def __iter__(self) -> Iterator[Goose]:
        return iter(self._data)

    def __delitem__(self, i: int) -> None:
        if not isinstance(i, int):
            log_and_raise(WrongTypeError("Index must be an integer"))
        
        try:
            self._data.pop(i)
        except IndexError:
            log_and_raise(OutOfRangeError(f"Goose at index {i} not found"))
        
        logger.info(f"Goose number {i} deleted")

    def append(self, goose: Goose) -> None:
        if not isinstance(goose, Goose):
            log_and_raise(WrongTypeError("Goose must be a Goose object"))
        
        self._data.append(goose)
        logger.info(f"Goose appended: {goose}")

    def __repr__(self) -> str:
        return f"GooseCollection({self._data})"