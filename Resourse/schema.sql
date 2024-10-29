-- Таблица для чатов
CREATE TABLE IF NOT EXISTS chats (
    id BIGINT PRIMARY KEY,                                          -- Уникальный идентификатор чата
    chat_name TEXT,                                                 -- Название чата
    spam_mute_time FLOAT DEFAULT (60),                              -- Время мута в чате
    spam_message INT DEFAULT (10),                                  -- Колличество сообщений для мута
    spam_time INT DEFAULT (10),                                     -- Время за которое дается мут
    delete_pattern TEXT DEFAULT ('http[s]?://\S+|www\.\S+')         -- Паттерн для удаления сообщений
);

-- Таблица для ролей (уникальные роли для каждого чата)
CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    role_name TEXT,                          -- Название роли (например, 'admin', 'moderator')
    chat_id BIGINT REFERENCES chats(id),     -- Внешний ключ на чат, для которого эта роль
    UNIQUE (role_name, chat_id)              -- Уникальность названия роли внутри каждого чата
);

-- Таблица для команд (каждый чат может иметь свой уникальный набор команд)
CREATE TABLE IF NOT EXISTS commands (
    id SERIAL PRIMARY KEY,
    command TEXT,                            -- Как команда вызывается пользователем (например, '/ban')
    command_name TEXT,                       -- Название команды (например, 'ban')
    description TEXT,                        -- Описание команды
    chat_id BIGINT REFERENCES chats(id),     -- Внешний ключ на чат, где используется команда
    UNIQUE (command, chat_id)                -- Уникальность команды внутри чата
);

-- Таблица для прав ролей (связь ролей с командами внутри чата)
CREATE TABLE IF NOT EXISTS role_permissions (
    role_id INT REFERENCES roles(id),        -- Внешний ключ на роль
    command_id INT REFERENCES commands(id),  -- Внешний ключ на команду
    PRIMARY KEY (role_id, command_id)        -- Уникальная комбинация роли и команды
);

-- Таблица для пользователей
CREATE TABLE IF NOT EXISTS users (
    id BIGINT PRIMARY KEY,                   -- Уникальный идентификатор пользователя
    username TEXT                           -- Имя пользователя
);

-- Таблица для связей между пользователями и чатами (многие ко многим)
CREATE TABLE IF NOT EXISTS user_chats (
    user_id BIGINT REFERENCES users(id),    -- Внешний ключ на пользователя
    chat_id BIGINT REFERENCES chats(id),    -- Внешний ключ на чат
    role_id BIGINT REFERENCES roles(id),    -- Внешний ключ на роль, которую пользователь выполняет в чате
    join_date TIMESTAMP DEFAULT NOW(),      -- Дата присоединения
    PRIMARY KEY (user_id, chat_id),         -- Уникальная комбинация пользователя и чата (у пользователя может быть только одна роль в одном чате)
    UNIQUE (user_id, chat_id)               -- Уникальность связи пользователя с чатом
);

-- Таблица для сообщений
CREATE TABLE IF NOT EXISTS messages (
    id BIGSERIAL PRIMARY KEY,              -- Автоинкрементируемый первичный ключ
    message_id BIGINT,                     -- Уникальный идентификатор сообщения
    user_id BIGINT REFERENCES users(id),   -- Внешний ключ на пользователя
    chat_id BIGINT REFERENCES chats(id),   -- Внешний ключ на чат
    message TEXT,                          -- Текст сообщения
    message_type TEXT DEFAULT 'text',      -- Тип сообщения (например, текст, изображение)
    date TIMESTAMP DEFAULT NOW()           -- Дата сообщения
);

CREATE TABLE IF NOT EXISTS muted_users (
    user_id BIGINT,
    chat_id BIGINT,
    mute_end TIMESTAMP,
    PRIMARY KEY (user_id, chat_id),
    FOREIGN KEY (chat_id) REFERENCES chats(id)
);

CREATE OR REPLACE FUNCTION insert_standard_roles_and_commands()
        RETURNS TRIGGER AS $$
        BEGIN

            -- Вставляем стандартные роли
            INSERT INTO roles (role_name, chat_id) 
            VALUES 
                ('admin', NEW.id), 
                ('moderator', NEW.id), 
                ('user', NEW.id);
            
            -- Вставляем стандартные команды
            INSERT INTO commands (command, command_name, description, chat_id) 
            VALUES 
                ('/start', 'start', 'Запустить бота', NEW.id),
                ('/help', 'help', 'Получить помощь', NEW.id),
                ('/mute', 'mute', 'Заглушить пользователя', NEW.id),
                ('/kick', 'kick', 'Выгнать пользователя', NEW.id),
                ('/unban', 'unban', 'Разбанить пользователя', NEW.id),
                ('/delete', 'delete_message', 'Удалить сообщение пользователя', NEW.id),
                ('/info', 'info', 'Информация о создателе', NEW.id),
                ('/ban', 'ban', 'Забанить пользователя', NEW.id),
                ('/unmute', 'unmute', 'Снять заглушение пользователя', NEW.id);

            -- Добавляем разрешения для ролей
            -- Администратор получает доступ ко всем командам
            INSERT INTO role_permissions (role_id, command_id)
            SELECT r.id, c.id 
            FROM roles r, commands c 
            WHERE r.chat_id = NEW.id AND r.role_name = 'admin';

            -- Модератор получает доступ только к некоторым командам
            INSERT INTO role_permissions (role_id, command_id)
            SELECT r.id, c.id 
            FROM roles r, commands c 
            WHERE r.chat_id = NEW.id AND r.role_name = 'moderator' 
            AND c.command IN ('/mute', '/kick', '/unmute', '/delete', '/start', '/info', '/help');

            -- Пользователь получает доступ только к стартовым командам
            INSERT INTO role_permissions (role_id, command_id)
            SELECT r.id, c.id 
            FROM roles r, commands c 
            WHERE r.chat_id = NEW.id AND r.role_name = 'user' 
            AND c.command IN ('/start', '/help', '/info');

            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;

        -- Триггер срабатывает при вставке нового чата
CREATE OR REPLACE TRIGGER trigger_insert_roles_and_commands
AFTER INSERT ON chats
FOR EACH ROW
EXECUTE FUNCTION insert_standard_roles_and_commands();

CREATE OR REPLACE FUNCTION check_spam_violation()
RETURNS TRIGGER AS $$
DECLARE
    mute_duration FLOAT;
    max_messages INT;
    time_window INT;
    last_message_time TIMESTAMP;
BEGIN
    -- Получаем параметры из таблицы чата
    SELECT spam_mute_time, spam_message, spam_time
    INTO mute_duration, max_messages, time_window
    FROM chats
    WHERE id = NEW.chat_id;

    -- Получаем время последнего сообщения пользователя
    SELECT MAX(date) INTO last_message_time
    FROM messages
    WHERE user_id = NEW.user_id
    AND chat_id = NEW.chat_id;

    -- Проверяем количество сообщений пользователя
    IF (SELECT COUNT(*) FROM messages
        WHERE user_id = NEW.user_id
        AND chat_id = NEW.chat_id
        AND date > (last_message_time - INTERVAL '1 second' * time_window)
       ) >= max_messages THEN
        
        -- Добавляем в таблицу muted_users
        INSERT INTO muted_users (user_id, chat_id, mute_end)
        VALUES (NEW.user_id, NEW.chat_id, last_message_time + INTERVAL '1 second' * mute_duration)
        ON CONFLICT (user_id, chat_id) DO UPDATE
        SET mute_end = last_message_time + INTERVAL '1 second' * mute_duration;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER spam_violation_check
AFTER INSERT ON messages
FOR EACH ROW
EXECUTE FUNCTION check_spam_violation();
