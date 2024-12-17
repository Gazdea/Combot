from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from alembic_utils.replaceable_entity import register_entities
from app.resource import schemas
import sys
import os
from app.config import url

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.model.Entity import Base 

config = context.config
fileConfig(config.config_file_name)

target_metadata = Base.metadata

register_entities([schemas.INSERT_STANDARD_ROLES_AND_COMMANDS_FN, schemas.CHECK_SPAM_VIOLATION_FN, schemas.CHECK_SPAM_VIOLATION_TG, schemas.INSERT_STANDARD_ROLES_AND_COMMANDS_TG])

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        url=url,
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()
    
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

