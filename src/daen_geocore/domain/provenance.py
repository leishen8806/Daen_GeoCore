from dataclasses import dataclass
from typing import Any

from .typed_values import TypedValue


@dataclass(frozen=True, slots=True)
class Provenance:
    """Open originating source context for a fact or representation.

    This is not mutation provenance, mutation audit, a Source resource,
    authorization data, provider ranking, or trust scoring.
    """

    source_context: Any = None
    details: tuple[TypedValue[Any], ...] = ()
