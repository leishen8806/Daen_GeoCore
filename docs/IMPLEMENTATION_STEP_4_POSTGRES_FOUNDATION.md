# Step 4 PostgreSQL Foundation

Step 4 provides the provider-neutral persistence foundation for the frozen
architecture. It uses SQLAlchemy Core 2.x with psycopg 3 against PostgreSQL 17.

- Production metadata is an empty infrastructure `MetaData`; no DAEN Domain tables are created.
- The engine factory uses runtime `DAEN_DATABASE_URL`, pool pre-ping, and read or mutation profiles.
- Read transactions use READ COMMITTED; mutation transactions use SERIALIZABLE.
- `PostgresUnitOfWork` owns one explicit local transaction and deterministic resource cleanup.
- Commit translation preserves committed, definitely-not-committed, and outcome-unknown states.
- Serialization and deadlock aborts map to retryable technical failures; indeterminate commit remains unknown.
- Alembic targets the empty production metadata for future revisions.
- Real PostgreSQL integration tests use a test-only probe table and `DAEN_TEST_DATABASE_URL`.
- Domain schema, repositories, APIs, provider adapters, and deployment remain deferred.
