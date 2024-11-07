import logging
from typing import Generator
from contextlib import contextmanager
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
import urllib.parse
import os

engine = create_engine(f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{urllib.parse.quote_plus(os.getenv('POSTGRES_PASSWORD'))}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def session_scope()-> Generator[Session, None, None]:
    """Контекстный менеджер для работы с сессией."""
    session = SessionLocal()
    try:
        yield session
    except Exception as e:
        logging.error(f'Error occurred: {e}', exc_info=True)
        session.rollback()
        raise e
    finally:
        session.close()
        
def get_session() -> Session:
    return SessionLocal()