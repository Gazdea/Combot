import os
import logging
import asyncpg
import asyncio

class DBConnectionPool:
    _pool = None

    @classmethod
    async def initialize(cls, minconn=1, maxconn=10):
        if cls._pool is None:
            cls._pool = await asyncpg.create_pool(
                database=os.getenv('POSTGRES_DB'),
                user=os.getenv('POSTGRES_USER'),
                password=os.getenv('POSTGRES_PASSWORD'),
                host=os.getenv('POSTGRES_HOST'),
                port=os.getenv('POSTGRES_PORT'),
                min_size=minconn,
                max_size=maxconn
            )

    @classmethod
    async def get_connection(cls):
        return await cls._pool.acquire()

    @classmethod
    def return_connection(cls, conn):
        return cls._pool.release(conn)

    @classmethod 
    async def close_all_connections(cls):
        await cls._pool.close()



async def execute_schema_file(schema_file_path):
    """Выполняет SQL команды из файла schema.sql"""
    conn = await DBConnectionPool.get_connection()
    try:
        with open(schema_file_path, 'r') as file:
            sql_script = file.read()

        await conn.execute(sql_script)
        logging.info("Таблицы успешно созданы из файла schema.sql.")
    except Exception as e:
        logging.error(f"Ошибка выполнения скрипта: {e}")
    finally:
        await DBConnectionPool.return_connection(conn)


async def add_chat(chat_id):
    """Добавляет новый чат в базу данных, если его еще нет."""
    try:
        chat_id = int(chat_id)
    except ValueError:
        logging.error(f"Некорректный chat_id: {chat_id}")
        return
    
    conn = await DBConnectionPool.get_connection()
    try:
        await conn.execute("""
            INSERT INTO chats (id)
            VALUES ($1)
            ON CONFLICT DO NOTHING;
        """, chat_id)
    except Exception as e:
        logging.error(f"Ошибка добавления чата: {e}")
    finally:
        await DBConnectionPool.return_connection(conn)


async def add_user(user, chat_id, role_name="user"):
    """Добавляет пользователя и связывает его с чатом в базе данных, если его еще нет."""
    conn = await DBConnectionPool.get_connection()
    try:
        await conn.execute("""
            INSERT INTO users (id, username, role_id)
            VALUES ($1, $2, (SELECT id FROM roles WHERE role_name = $3))
            ON CONFLICT (id) DO NOTHING;
        """, user.id, user.username, role_name)

        await conn.execute("""
            INSERT INTO user_chats (user_id, chat_id)
            VALUES ($1, $2)
            ON CONFLICT DO NOTHING;
        """, user.id, chat_id)
    except Exception as e:
        logging.error(f"Ошибка добавления пользователя: {e}")
    finally:
        await DBConnectionPool.return_connection(conn)


async def add_chat_and_users(chat_id, user_list):
    """Добавляет новый чат и всех пользователей в этот чат."""
    await add_chat(chat_id)
    for user in user_list:
        await add_user(user, chat_id)


async def log_message(user_id, chat_id, message_text, message_type="text"):
    """Логирует сообщение пользователя в базе данных."""
    conn = await DBConnectionPool.get_connection()
    try:
        await conn.execute("""
            INSERT INTO messages (user_id, chat_id, message, message_type)
            VALUES ($1, $2, $3, $4);
        """, user_id, chat_id, message_text, message_type)
    except Exception as e:
        logging.error(f"Ошибка логирования сообщения: {e}")
    finally:
        await DBConnectionPool.return_connection(conn)


async def get_user_role(user_id):
    """Получает роль пользователя по его ID."""
    conn = await DBConnectionPool.get_connection()
    try:
        role = await conn.fetchval("""
            SELECT role_name FROM roles
            JOIN users ON users.role_id = roles.id
            WHERE users.id = $1;
        """, user_id)
        return role
    except Exception as e:
        logging.error(f"Ошибка получения роли пользователя: {e}")
        return None
    finally:
        await DBConnectionPool.return_connection(conn)

async def get_user_id(user_tag):
    """Получить id пользователя по его нику"""
    conn = await DBConnectionPool.get_connection()
    try:
        user_id = await conn.fetchval("""
            SELECT id FROM users
            WHERE username = $1;
        """, user_tag)
        return user_id
    except Exception as e:
        logging.error(f"Ошибка получения id пользователя: {e}")
        return None
    finally:
        await DBConnectionPool.return_connection(conn)

async def remove_user(user_id):
    """Удаляет пользователя по ID."""
    conn = await DBConnectionPool.get_connection()
    try:
        result = await conn.execute("DELETE FROM users WHERE id = $1 RETURNING id", user_id)
        return result is not None
    except Exception as e:
        logging.error(f"Ошибка удаления пользователя: {e}")
        return False
    finally:
        await DBConnectionPool.return_connection(conn)

# Инициализация пула соединений
async def main():
    await DBConnectionPool.initialize()
    await execute_schema_file('db/schema.sql')  # Замените на путь к вашему файлу

if __name__ == "__main__":
    asyncio.run(main())
