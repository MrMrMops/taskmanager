from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import create_engine
from alembic import context
from api.core.config import settings
from api.db.database import Base

# Конфигурация логирования
if context.config.config_file_name:
    fileConfig(context.config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Запуск миграций в оффлайн-режиме."""
    url = settings.ASYNC_DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Запуск миграций в онлайн-режиме."""
    connectable = create_engine(
        settings.ASYNC_DATABASE_URL,
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