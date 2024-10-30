CREATE OR REPLACE FUNCTION insert_standard_roles_and_commands()
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
        ...
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

CREATE TRIGGER trigger_insert_roles_and_commands
AFTER INSERT ON chats
FOR EACH ROW
EXECUTE FUNCTION insert_standard_roles_and_commands();