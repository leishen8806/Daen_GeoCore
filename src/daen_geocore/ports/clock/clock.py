from datetime import datetime
from typing import Protocol


class Clock(Protocol):
    """UTC recorded-time metadata only; not basis, ordering, LWW, or consensus."""

    def now(self) -> datetime: ...
