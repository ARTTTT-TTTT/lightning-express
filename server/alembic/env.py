import sys
import os
from logging.config import fileConfig

from sqlalchemy import create_engine, pool

from alembic import context

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.configs.app_config import app_config
from app.database.base import Base

from app.models import *  # type: ignore # noqa: F403

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

def get_url():
    """
    Retrieves the database URL from app_config and adjusts it for Alembic's
    synchronous engine. Specifically, it removes the '+asyncpg' dialect part
    if present, as Alembic's create_engine expects a synchronous dialect.
    """
    database_url = str(app_config.SQLALCHEMY_DATABASE_URI)
    # Remove the '+asyncpg' part for Alembic's synchronous engine
    if database_url.startswith("postgresql+asyncpg://"):
        return database_url.replace("postgresql+asyncpg://", "postgresql://")
    # If using psycopg (synchronous driver), it can be used directly
    # If using other async drivers, add similar replacement logic here
    return database_url


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode using FastAPI config."""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode using FastAPI config."""
    connectable = create_engine(
        get_url(),
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
