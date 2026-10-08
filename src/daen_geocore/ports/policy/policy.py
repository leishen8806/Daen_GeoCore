from typing import Protocol

from daen_geocore.ports.result import PortResult


class PolicyHook(Protocol):
    """Minimal policy hook; policy vocabulary and authorization remain open."""

    def evaluate(self, context: object) -> PortResult[None]: ...
