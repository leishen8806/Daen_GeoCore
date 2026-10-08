from datetime import datetime
from typing import Protocol


class Clock(Protocol):
    """Time source port; callers decide whether time is operational metadata."""

    def now(self) -> datetime: ...
