from importlib.readers import FileReader
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Создаем базовый класс для моделей
Base = declarative_base()

class DBConnection:
    _engine = None
    _SessionLocal = None

    @classmethod
    def initialize(cls):
        """Инициализация подключения к базе данных."""
        if cls._engine is None:
            cls._engine = create_engine(
                f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}",
                echo=True  # Установите в True, чтобы видеть SQL-запросы в консоли
            )
            cls._SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=cls._engine)

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
        """Создает все таблицы в базе данных и триггер."""
        if cls._engine is None:
            cls.initialize()
        Base.metadata.create_all(bind=cls._engine)

        # Создаем сессию
        session = cls.get_session()()

        # SQL-запрос для создания триггера
        sql_script = ''
        try:
            # Выполнение SQL-запроса для создания триггера
            with open('db/schema.sql', 'r') as file:
                sql_script = file.read()
            session.execute(sql_script)
            session.commit()
        except Exception as e:
            print(f"Ошибка при создании триггера: {e}")
            session.rollback()
        finally:
            # Закрытие сессии
            cls.close_session(session)
