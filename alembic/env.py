from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
import sqlalchemy as sa
from alembic import context, op
from alembic_utils.replaceable_entity import register_entities
from sqlalchemy.dialects import postgresql
import alembic_postgresql_enum


from app.resource import schemas
from app.config import get_url

from app.db.model.Entity import Base

config = context.config
fileConfig(config.config_file_name)

target_metadata = Base.metadata

register_entities([schemas.CHECK_SPAM_VIOLATION_FN, schemas.CHECK_SPAM_VIOLATION_TG])

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(url=get_url(), target_metadata=target_metadata, literal_binds=True)
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

user_role_enum = postgresql.ENUM('GUEST', 'USER', 'MODERATOR', 'ADMIN', name='user_role')

def upgrade():
    user_role_enum.create(op.get_bind(), checkfirst=True)
    op.add_column('roles',  sa.Column('role', user_role_enum, nullable=False))

def downgrade():
    op.drop_column('roles',  'role')
    user_role_enum.drop(op.get_bind(), checkfirst=True)

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

