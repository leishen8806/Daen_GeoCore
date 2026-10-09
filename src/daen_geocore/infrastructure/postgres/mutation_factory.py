from sqlalchemy import Engine

from daen_geocore.infrastructure.postgres.engine import TransactionProfile, create_postgres_engine
from daen_geocore.infrastructure.postgres.uow import PostgresUnitOfWork


class PostgresMutationUnitOfWorkFactory:
    def __init__(self, database_url: str) -> None:
        self._engine: Engine = create_postgres_engine(database_url, TransactionProfile.MUTATION)

    def create(self) -> PostgresUnitOfWork:
        return PostgresUnitOfWork(self._engine)
