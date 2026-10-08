"""Alembic environment for the empty infrastructure metadata baseline."""

from logging.config import fileConfig

from alembic import context

from daen_geocore.infrastructure.postgres.engine import create_postgres_engine
from daen_geocore.infrastructure.postgres.metadata import metadata
from daen_geocore.infrastructure.runtime.settings import RuntimeSettings

config = context.config
if config.config_file_name is not None and config.get_section("loggers") is not None:
    fileConfig(config.config_file_name)

target_metadata = metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url") or RuntimeSettings().database_url
    options = {
        "target_metadata": target_metadata,
        "literal_binds": True,
        "dialect_opts": {"paramstyle": "named"},
    }
    if url:
        options["url"] = url
    else:
        options["dialect_name"] = "postgresql"
    context.configure(
        **options,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    url = config.get_main_option("sqlalchemy.url") or RuntimeSettings().database_url
    if not url:
        raise RuntimeError("DAEN_DATABASE_URL is required for online Alembic commands")
    connectable = create_postgres_engine(url)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
