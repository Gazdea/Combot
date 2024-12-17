RETURNS TRIGGER AS $$
BEGIN
    -- Вставляем стандартные роли
    INSERT INTO roles (role_name, chat_id) VALUES 
        ('admin', NEW.id), 
        ('moderator', NEW.id), 
        ('user', NEW.id);
    -- Вставляем стандартные команды
    INSERT INTO commands (command, method_name, description, chat_id) VALUES 
                ('/start', 'start', 'Запустить бота {noArgs}', NEW.id),
                ('/info', 'info', 'Информация о создателе {noArgs}', NEW.id),

                ('/kick', 'user_kick', 'Выгнать пользователя {argUsername, argInfoReason}', NEW.id),
                ('/ban', 'user_ban', 'Забанить пользователя {argUsername, argDateTime, argInfoReason}', NEW.id),
                ('/unban', 'user_unban', 'Разбанить пользователя {argUsername}', NEW.id),
                ('/mute', 'user_mute', 'Заглушить пользователя {argUsername, argDateTime, argInfoReason}', NEW.id),
                ('/unmute', 'user_unmute', 'Снять заглушение пользователя {argUsername}', NEW.id),
                ('/userRole', 'user_role', 'Устаноить пользователю роль {argUsername, argInfoRole}', NEW.id),
                ('/userInfo', 'user_info', 'Получить информацию о юзере {argUsername}', NEW.id),
                ('/usersJoin', 'chat_user_join', 'Получить статистику о подключившихся пользователях {noArgs, argDateTime}', NEW.id),
                ('/usersActive', 'chat_user_active', 'Получить статистику активных пользователей {noArgs, argDateTime}', NEW.id),
    
                ('/delete', 'delete_message', 'Удалить сообщение пользователя {argMessage}', NEW.id),

                ('/chatSpamMuteTime', 'chat_spam_mute_time', 'Установить время мута в чате {argInfo}', NEW.id),
                ('/chatSpamNumMessage', 'chat_spam_num_message', 'Установить колличество сообщения для мута {argInfo}', NEW.id),
                ('/chatSpamTime', 'chat_spam_time', 'Установить время подсчитывания сообщений {argInfo}', NEW.id),
                ('/chatdeletePatternSet', 'chat_delete_pattern', 'Установить паттерн удаляемых сообщений {argInfo}', NEW.id),

                ('/roles', 'role_list', 'Получить информацию о роли {argInfoRole}', NEW.id),
                ('/roleRename', 'role_rename', 'Изменить название роли {argInfoRole, argInfo}', NEW.id),
                ('/roleAdd', 'role_add', 'Добавить роль {argInfoRole}', NEW.id),
                ('/roleDelete', 'role_delete', 'Удалить роль {argInfoRole}', NEW.id),
                ('/roleCommands', 'commands_role', 'Получить команды для роли {argInfoRole}', NEW.id),
                ('/roleCommandAdd', 'role_command_add', 'Добавить команду для роли {argInfoRole, argInfoCommand}', NEW.id),
                ('/roleCommandDelete', 'role_command_delete', 'Удалить команду для роли {argInfoRole, argInfoCommand}', NEW.id),

                ('/commandRename', 'command_rename', 'Изменить название команды {argInfoCommand, argInfo}', NEW.id),
                ('/help', 'help', 'Получить список возможных команд {noArgs, argInfoCommand}', NEW.id);

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
