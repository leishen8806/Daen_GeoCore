from dataclasses import dataclass
from typing import Any

from .typed_values import TypedValue


@dataclass(frozen=True, slots=True)
class Quality:
    """Open fact-quality context with explicit unknown state."""

    dimensions: tuple[TypedValue[Any], ...] = ()

    @classmethod
    def unknown(cls) -> "Quality":
        return cls()
