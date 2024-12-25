import logging
from typing import Generator
from contextlib import contextmanager
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import Engine, create_engine
import urllib.parse
import os

postgres_user = os.getenv('POSTGRES_USER', 'user')
postgres_password = os.getenv('POSTGRES_PASSWORD', 'pass')
postgres_host = os.getenv('POSTGRES_HOST', 'localhost')
postgres_port = os.getenv('POSTGRES_PORT', '5432')
postgres_db = os.getenv('POSTGRES_DB', 'postgres')

postgres_password = urllib.parse.quote_plus(postgres_password) if postgres_password else ''

url = f"postgresql+psycopg2://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"

engine = create_engine(url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def session_scope()-> Generator[Session, None, None]:
    """
    Provide a transactional scope for database operations.

    This context manager yields a SQLAlchemy database session, ensuring that
    the session is committed if no exceptions occur, or rolled back if an
    exception is raised. It also handles session cleanup by closing it
    after use.

    Yields:
        Session: A SQLAlchemy session object for performing database operations.

    Raises:
        Exception: Propagates any exception that occurs during the session
        and logs the error.
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        logging.error(f'Error occurred: {e}', exc_info=True)
        session.rollback()
        raise e
    finally:
        session.close()
        
def get_session() -> Session:
    """
    Get a new database session.

    This function provides a convenient way to get a new database session for
    performing operations that are not wrapped in a transactional context using
    the :func:`session_scope` context manager.

    Returns:
        Session: A new SQLAlchemy session object for performing database operations.
    """
    return SessionLocal()

def get_url() -> str:
    return url

def get_engine() -> Engine:
    return engine