RETURNS TRIGGER AS $$
BEGIN
    -- Вставляем стандартные роли
    INSERT INTO roles (role_name, chat_id) VALUES 
        ('admin', NEW.id), 
        ('moderator', NEW.id), 
        ('user', NEW.id);
    -- Вставляем стандартные команды
    INSERT INTO commands (command, command_name, description, chat_id) VALUES 
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
                ('/chatSpamNumMessageSet', 'chat_spam_num_message_set', 'Установить колличество сообщения для мута', NEW.id),
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

    -- Разрешения для ролей (admin, moderator, user)
    INSERT INTO role_permissions (role_id, command_id)
    SELECT r.id, c.id 
    FROM roles r, commands c 
    WHERE r.chat_id = NEW.id AND r.role_name = 'admin';

    INSERT INTO role_permissions (role_id, command_id)
    SELECT r.id, c.id 
    FROM roles r, commands c 
    WHERE r.chat_id = NEW.id AND r.role_name = 'moderator'
    AND c.command IN ('/mute', '/kick', '/unmute', '/delete', '/start', '/info', '/help');

    INSERT INTO role_permissions (role_id, command_id)
    SELECT r.id, c.id 
    FROM roles r, commands c 
    WHERE r.chat_id = NEW.id AND r.role_name = 'user'
    AND c.command IN ('/start', '/help', '/info');

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
