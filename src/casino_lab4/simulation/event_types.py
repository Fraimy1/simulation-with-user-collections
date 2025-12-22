from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Protocol, TypeAlias

from casino_lab4.simulation.casino import Casino


class EventHandler(Protocol):
    def __call__(self, casino: Casino) -> None: ...


EventCondition: TypeAlias = Callable[[Casino], bool]


def _always(_: Casino) -> bool:
    return True


@dataclass(frozen=True, slots=True)
class Event:
    name: str
    handler: EventHandler
    weight: float = 1.0
    enabled: EventCondition = field(default=_always)
