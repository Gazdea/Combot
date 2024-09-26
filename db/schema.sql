-- Таблица для ролей
CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    role_name TEXT UNIQUE
);

-- Таблица для пользователей
CREATE TABLE IF NOT EXISTS users (
    id BIGINT PRIMARY KEY,           -- Идентификатор пользователя
    username TEXT,                   -- Имя пользователя
    join_date TIMESTAMP DEFAULT NOW(), -- Дата присоединения
    role_id INT REFERENCES roles(id) DEFAULT 3 -- Внешний ключ на роль
);

-- Таблица для чатов
CREATE TABLE IF NOT EXISTS chats (
    id BIGINT PRIMARY KEY,           -- ID чата
    chat_name TEXT                   -- Название чата (может быть полезно для групп)
);

-- Таблица для сообщений
CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,           -- Уникальный идентификатор сообщения
    user_id BIGINT REFERENCES users(id), -- Внешний ключ на пользователя
    chat_id BIGINT REFERENCES chats(id), -- Внешний ключ на чат
    message TEXT,                    -- Текст сообщения
    message_type TEXT DEFAULT 'text', -- Тип сообщения (например, текст, изображение)
    date TIMESTAMP DEFAULT NOW()      -- Дата сообщения
);

-- Таблица для связей между пользователями и чатами (многие ко многим)
CREATE TABLE IF NOT EXISTS user_chats (
    user_id BIGINT REFERENCES users(id), -- Внешний ключ на пользователя
    chat_id BIGINT REFERENCES chats(id), -- Внешний ключ на чат
    PRIMARY KEY (user_id, chat_id)        -- Первичный ключ — комбинация пользователя и чата
);

-- Вставляем роли админа, модератора и пользователя
INSERT INTO roles (role_name) VALUES ('admin'), ('moderator'), ('user') ON CONFLICT DO NOTHING;
