from enum import StrEnum

from sqlalchemy import Engine, create_engine

from daen_geocore.infrastructure.runtime.settings import RuntimeSettings


class TransactionProfile(StrEnum):
    READ = "read"
    MUTATION = "mutation"


def create_postgres_engine(
    database_url: str,
    profile: TransactionProfile = TransactionProfile.READ,
) -> Engine:
    if not database_url:
        raise ValueError("DAEN_DATABASE_URL is required")
    isolation = "SERIALIZABLE" if profile is TransactionProfile.MUTATION else "READ COMMITTED"
    return create_engine(
        database_url,
        pool_pre_ping=True,
        execution_options={"isolation_level": isolation},
    )


def create_engine_from_settings(
    settings: RuntimeSettings,
    profile: TransactionProfile = TransactionProfile.READ,
) -> Engine:
    return create_postgres_engine(settings.database_url, profile)
