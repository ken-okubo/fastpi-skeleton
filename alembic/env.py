# fmt: off

import os
import sys

sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '')))

from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context

# Importa a Base e os modelos para registrar metadata
from app.core.db import Base
from app.models import user  # noqa: F401

# fmt: on

config = context.config

# Configura o log
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata dos modelos para autogenerate funcionar
target_metadata = Base.metadata


def get_database_url():
    env_url = os.getenv("DATABASE_URL")
    if env_url:
        if env_url.startswith("postgres://"):
            env_url = env_url.replace("postgres://", "postgresql://", 1)
        return env_url

    ini_url = config.get_main_option("sqlalchemy.url")
    print(f"No DATABASE_URL env found, using alembic.ini: {ini_url}")
    return ini_url


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = get_database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        {"sqlalchemy.url": get_database_url()},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
