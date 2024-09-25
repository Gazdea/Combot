CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    role_name TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS users (
    id BIGINT PRIMARY KEY,
    username TEXT,
    chat_id BIGINT,
    join_date TIMESTAMP DEFAULT NOW(),
    role_id INT REFERENCES roles(id)
);

CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id),
    message TEXT,
    message_type TEXT DEFAULT 'text',
    date TIMESTAMP DEFAULT NOW()
);

-- Вставляем роли админа, модератора и пользователя
INSERT INTO roles (role_name) VALUES ('admin'), ('moderator'), ('user') ON CONFLICT DO NOTHING;
