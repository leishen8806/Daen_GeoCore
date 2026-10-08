from collections.abc import Mapping
from typing import Protocol


class ObservabilityPort(Protocol):
    """Provider-neutral operational telemetry hooks."""

    def event(self, name: str, attributes: Mapping[str, object] | None = None) -> None: ...

    def exception(
        self, error: BaseException, attributes: Mapping[str, object] | None = None
    ) -> None: ...
