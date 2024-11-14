import logging
from typing import Generator
from contextlib import contextmanager
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
import urllib.parse
import os

url = f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{urllib.parse.quote_plus(os.getenv('POSTGRES_PASSWORD'))}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
engine = create_engine(url)
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


