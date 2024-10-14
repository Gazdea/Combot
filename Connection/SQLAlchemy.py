import logging
import os
import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Создаем базовый класс для моделей
Base = declarative_base()

# Настройка логирования
logging.basicConfig(level=logging.INFO)

class DBConnection:
    _engine = None
    _SessionLocal = None
    
    @classmethod
    def initialize(cls):
        """Инициализация подключения к базе данных."""
        if cls._engine is None:
            try:
                logging.info("Инициализация подключения к базе данных.")
                # Формирование строки подключения с использованием переменных окружения
                cls._engine = create_engine(
                    f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{urllib.parse.quote_plus(os.getenv('POSTGRES_PASSWORD'))}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}",
                    echo=True,
                    client_encoding='utf8',  # Устанавливаем кодировку на уровне клиента
                )
                cls._SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=cls._engine)
            except Exception as e:
                logging.error(f"Ошибка при подключении к базе данных: {e}")
                raise

    @classmethod
    def get_session(cls):
        """Создает новую сессию для взаимодействия с базой данных."""
        if cls._SessionLocal is None:
            cls.initialize()
        return cls._SessionLocal()

    @classmethod
    def close_session(cls, session):
        """Закрывает сессию."""
        session.close()

    @classmethod
    def create_all_tables(cls):
        """Создает все таблицы в базе данных и выполняет скрипт для создания триггеров."""
        if cls._engine is None:
            cls.initialize()

        # Создаем все таблицы, используя метаданные из моделей
        Base.metadata.create_all(bind=cls._engine)

        # Создаем сессию
        session = cls.get_session()

        try:
            # Выполняем SQL-скрипт для создания триггеров
            execute_sql_script(session, 'Resourse/schema.sql')
        except Exception as e:
            logging.error(f"Ошибка при создании триггеров: {e}")
        finally:
            # Закрываем сессию в любом случае
            cls.close_session(session)

def execute_sql_script(session, script_path):
    """Выполняет SQL-скрипт, разделяя его на отдельные команды."""
    try:
        with open(script_path, 'r', encoding="utf-8", errors='ignore') as file:
            sql_script = file.read()

            session.execute(sql_script)
        session.commit()
        logging.info(f"SQL-скрипт успешно выполнен из файла: {script_path}")
    except Exception as e:
        logging.error(f"Ошибка при выполнении SQL-скрипта: {e}")
        session.rollback()
        raise
