import psycopg2
from psycopg2 import pool
import os
import logging

class DBConnectionPool:
    _pool = None

    @classmethod
    def initialize(cls, minconn=1, maxconn=10):
        if cls._pool is None:
            cls._pool = psycopg2.pool.SimpleConnectionPool(
                minconn, maxconn,
                dbname=os.getenv('POSTGRES_DB'),
                user=os.getenv('POSTGRES_USER'),
                password=os.getenv('POSTGRES_PASSWORD'),
                host=os.getenv('POSTGRES_HOST'),
                port=os.getenv('POSTGRES_PORT')
            )

    @classmethod
    def get_connection(cls):
        return cls._pool.getconn()

    @classmethod
    def return_connection(cls, conn):
        cls._pool.putconn(conn)

    @classmethod
    def close_all_connections(cls):
        cls._pool.closeall()

def execute_schema_file(schema_file_path):
    """Выполняет SQL команды из файла schema.sql"""
    conn = DBConnectionPool.get_connection()
    try:
        with open(schema_file_path, 'r') as file:
            sql_script = file.read()

        with conn.cursor() as cur:
            cur.execute(sql_script)

        conn.commit()
        logging.info("Таблицы успешно созданы из файла schema.sql.")
    except Exception as e:
        logging.error(f"Ошибка выполнения скрипта: {e}")
        conn.rollback()
    finally:
        DBConnectionPool.return_connection(conn)

# Инициализация пула соединений
DBConnectionPool.initialize()

# Выполнение SQL-схемы
execute_schema_file('db/schema.sql')  # Замените на путь к вашему файлу

def add_user(user_id, username, chat_id, role_name="user"):
    """Добавляет пользователя в базу данных, если его еще нет."""
    conn = DBConnectionPool.get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO users (id, username, chat_id, role_id)
                VALUES (%s, %s, %s, (SELECT id FROM roles WHERE role_name = %s))
                ON CONFLICT (id) DO NOTHING;
            """, (user_id, username, chat_id, role_name))
            conn.commit()
    except Exception as e:
        logging.error(f"Ошибка добавления пользователя: {e}")
        conn.rollback()
    finally:
        DBConnectionPool.return_connection(conn)

def log_message(user_id, message_text, message_type="text"):
    """Логирует сообщение пользователя в базе данных."""
    conn = DBConnectionPool.get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO messages (user_id, message, message_type)
                VALUES (%s, %s, %s);
            """, (user_id, message_text, message_type))
            conn.commit()
    except Exception as e:
        logging.error(f"Ошибка логирования сообщения: {e}")
        conn.rollback()
    finally:
        DBConnectionPool.return_connection(conn)

def get_user_role(user_id):
    """Получает роль пользователя по его ID."""
    conn = DBConnectionPool.get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT role_name FROM roles
                JOIN users ON users.role_id = roles.id
                WHERE users.id = %s;
            """, (user_id,))
            role = cur.fetchone()
            return role[0] if role else None
    except Exception as e:
        logging.error(f"Ошибка получения роли пользователя: {e}")
        return None
    finally:
        DBConnectionPool.return_connection(conn)

def remove_user(user_id):
    """Удаляет пользователя по ID."""
    conn = DBConnectionPool.get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM users WHERE id = %s RETURNING id", (user_id,))
            result = cur.fetchone()
            conn.commit()
            return result is not None
    except Exception as e:
        logging.error(f"Ошибка удаления пользователя: {e}")
        conn.rollback()
        return False
    finally:
        DBConnectionPool.return_connection(conn)
