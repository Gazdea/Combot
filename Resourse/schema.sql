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
                ('/unmute', 'unmute', 'Снять заглушение пользователя', NEW.id),
                ('/chatSpamMuteTimeSet', 'chat_spam_mute_time_set', 'Установить время мута в чате', NEW.id),
                ('/chatSpamNumMessageSet', 'chat_spam_mum_message_set', 'Установить колличество сообщения для мута', NEW.id),
                ('/chatSpamTimeSet', 'chat_spam_time_set', 'Установить время подсчитывания сообщений', NEW.id),
                ('/chatdeletePatternSet', 'chat_delete_pattern_set', 'Установить паттерн удаляемых сообщений', NEW.id),
                ('/roleAdd', 'role_add', 'Добавить роль', NEW.id),
                ('/roleDelete', 'role_delete', 'Удалить роль', NEW.id),
                ('/roleCommandAdd', 'role_command_add', 'Добавить команду для роли', NEW.id),
                ('/roleCommandDelete', 'role_command_delete', 'Удалить команду для роли', NEW.id),
                ('/userRoleSet', 'role_user_set', 'Устаноить пользователю роль', NEW.id),
                ('/commandRename', 'command_rename', 'Изменить название команды', NEW.id),
                ('/chatUser', 'chat_user', 'Получить информацию о юзере', NEW.id),
                ('/chatStatsUserJoin', 'chat_stats_user_join', 'Получить статистику о подключившихся пользователях', NEW.id),
                ('/chatStatsUserActive', 'chat_stats_user_active', 'Получить статистику активных пользователей', NEW.id);

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
