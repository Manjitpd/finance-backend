import sys
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# 👇 Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# 👇 Import your Base and settings
from app.db.base import Base
from app.core.config import settings

# 👇 VERY IMPORTANT: import all models
from app.models import user, finance, role

# Alembic Config
config = context.config

# 👇 Override DB URL from .env
config.set_main_option("sqlalchemy.url", settings.SYNC_DATABASE_URL)
# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 👇 THIS IS CRITICAL
target_metadata = Base.metadata


# =========================
# OFFLINE MODE
# =========================
def run_migrations_offline() -> None:
    context.configure(
        url=settings.DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# =========================
# ONLINE MODE
# =========================
def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()