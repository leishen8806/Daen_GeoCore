from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class Provenance:
    """Minimal attributable source/mutation context carrier.

    This is intentionally open and does not model a Source resource,
    authorization, ranking, or mutation audit record.
    """

    recorded_by: Any = None
    context: Any = None
    affected_references: tuple[Any, ...] = ()
    evidence: Any = None
    resulting_references: tuple[Any, ...] = ()
