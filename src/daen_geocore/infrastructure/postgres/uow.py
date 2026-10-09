from __future__ import annotations

from sqlalchemy import Connection, Engine
from sqlalchemy.engine import RootTransaction

from daen_geocore.infrastructure.postgres.errors import (
    PostgresInfrastructureError,
    translate_begin_failure,
    translate_commit_failure,
)
from daen_geocore.ports.persistence.commit import (
    CommitAccepted,
    CommitOutcome,
    CommitUnknown,
)


class PostgresUnitOfWork:
    """Infrastructure-owned explicit transaction adapter."""

    def __init__(self, engine: Engine) -> None:
        self._engine = engine
        self._connection: Connection | None = None
        self._transaction: RootTransaction | None = None
        self._state = "new"
        self.last_outcome: CommitOutcome | None = None

    @property
    def state(self) -> str:
        return self._state

    def _require_connection(self) -> Connection:
        if self._connection is None or self._state != "active":
            raise RuntimeError("unit of work is not active")
        return self._connection

    @property
    def identity(self):
        from .repositories import PostgresIdentityRepository

        return PostgresIdentityRepository(self._require_connection())

    @property
    def assertions(self):
        from .repositories import PostgresAssertionsRepository

        return PostgresAssertionsRepository(self._require_connection())

    @property
    def representation(self):
        from .repositories import PostgresRepresentationRepository

        return PostgresRepresentationRepository(self._require_connection())

    def __enter__(self) -> PostgresUnitOfWork:
        self.begin()
        return self

    def __exit__(self, exc_type: object, exc_value: object, traceback: object) -> None:
        if self._state == "active":
            self.rollback()
        elif self._state not in {
            "committed",
            "not_committed",
            "unknown",
            "rolled_back",
            "closed",
        }:
            raise RuntimeError("unit of work is not active")
        self._close()

    def begin(self) -> None:
        if self._state != "new":
            raise RuntimeError("unit of work is not new")
        try:
            self._connection = self._engine.connect()
            self._transaction = self._connection.begin()
        except BaseException as error:
            self._close()
            raise PostgresInfrastructureError(translate_begin_failure(error)) from error
        self._state = "active"

    def commit(self) -> CommitOutcome:
        if self._state != "active" or self._transaction is None:
            raise RuntimeError("unit of work is not active")
        try:
            self._transaction.commit()
        except BaseException as error:
            outcome = translate_commit_failure(error)
            self.last_outcome = outcome
            self._state = "unknown" if isinstance(outcome, CommitUnknown) else "not_committed"
            self._close()
            return outcome
        self.last_outcome = CommitAccepted()
        self._state = "committed"
        self._close()
        return self.last_outcome

    def rollback(self) -> None:
        if self._state in {"committed", "closed", "unknown", "not_committed"}:
            raise RuntimeError("unit of work cannot roll back")
        if self._transaction is not None:
            self._transaction.rollback()
        self._state = "rolled_back"

    def _close(self) -> None:
        if self._connection is not None:
            self._connection.close()
        self._connection = None
        self._transaction = None
        if self._state in {"committed", "not_committed", "rolled_back"}:
            self._state = "closed"
