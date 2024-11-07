from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context, op
from alembic_utils.replaceable_entity import register_entities
from Resourse import schemas
import sys
import os
import urllib.parse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Models.Entity import Base 

config = context.config
fileConfig(config.config_file_name)

target_metadata = Base.metadata

register_entities([schemas.INSERT_STANDARD_ROLES_AND_COMMANDS_FN, schemas.CHECK_SPAM_VIOLATION_FN, schemas.CHECK_SPAM_VIOLATION_TG, schemas.INSERT_STANDARD_ROLES_AND_COMMANDS_TG])

def get_url():
    return f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{urllib.parse.quote_plus(os.getenv('POSTGRES_PASSWORD'))}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = get_url()
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        url=get_url(),
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
