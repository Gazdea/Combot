"""migration

Revision ID: f2a91b7825ad
Revises: 2e0bbc46afd9
Create Date: 2024-11-18 14:12:52.276757

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from alembic_utils.pg_function import PGFunction
from sqlalchemy import text as sql_text

# revision identifiers, used by Alembic.
revision: str = 'f2a91b7825ad'
down_revision: Union[str, None] = '2e0bbc46afd9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    public_insert_standard_roles_and_commands = PGFunction(
        schema="public",
        signature="insert_standard_roles_and_commands()",
        definition="RETURNS TRIGGER AS $$\nBEGIN\n    -- Вставляем стандартные роли\n    INSERT INTO roles (role_name, chat_id) VALUES \n        ('admin', NEW.id), \n        ('moderator', NEW.id), \n        ('user', NEW.id);\n    -- Вставляем стандартные команды\n    INSERT INTO commands (command, command_name, description, chat_id) VALUES \n                ('/start', 'start', 'Запустить бота {noArgs}', NEW.id),\n                ('/info', 'info', 'Информация о создателе {noArgs}', NEW.id),\n\n                ('/kick', 'user_kick', 'Выгнать пользователя {argUsername, argInfoReason}', NEW.id),\n                ('/ban', 'user_ban', 'Забанить пользователя {argUsername, argDateTime, argInfoReason}', NEW.id),\n                ('/unban', 'user_unban', 'Разбанить пользователя {argUsername}', NEW.id),\n                ('/mute', 'user_mute', 'Заглушить пользователя {argUsername, argDateTime, argInfoReason}', NEW.id),\n                ('/unmute', 'user_unmute', 'Снять заглушение пользователя {argUsername}', NEW.id),\n                ('/userRoleSet', 'user_role_set', 'Устаноить пользователю роль {argUsername, argInfoRole}', NEW.id),\n                ('/userInfo', 'user_info', 'Получить информацию о юзере {argUsername}', NEW.id),\n                ('/usersJoin', 'chat_user_join', 'Получить статистику о подключившихся пользователях {noArgs, argDateTime}', NEW.id),\n                ('/usersActive', 'chat_user_active', 'Получить статистику активных пользователей {noArgs, argDateTime}', NEW.id),\n    \n                ('/delete', 'delete_message', 'Удалить сообщение пользователя {argMessage}', NEW.id),\n\n                ('/chatSpamMuteTime', 'chat_spam_mute_time', 'Установить время мута в чате {argInfo}', NEW.id),\n                ('/chatSpamNumMessage', 'chat_spam_num_message', 'Установить колличество сообщения для мута {argInfo}', NEW.id),\n                ('/chatSpamTime', 'chat_spam_time', 'Установить время подсчитывания сообщений {argInfo}', NEW.id),\n                ('/chatdeletePatternSet', 'chat_delete_pattern', 'Установить паттерн удаляемых сообщений {argInfo}', NEW.id),\n\n                ('/roles', 'roles_list', 'Получить информацию о роли {argInfoRole}', NEW.id),\n                ('/roleRename', 'role_rename', 'Изменить название роли {argInfoRole, argInfo}', NEW.id),\n                ('/roleAdd', 'role_add', 'Добавить роль {argInfoRole}', NEW.id),\n                ('/roleDelete', 'role_delete', 'Удалить роль {argInfoRole}', NEW.id),\n                ('/roleCommands', 'commands_role', 'Получить команды для роли {argInfoRole}', NEW.id),\n                ('/roleCommandAdd', 'role_command_add', 'Добавить команду для роли {argInfoRole, argInfoCommand}', NEW.id),\n                ('/roleCommandDelete', 'role_command_delete', 'Удалить команду для роли {argInfoRole, argInfoCommand}', NEW.id),\n\n                ('/commandRename', 'command_rename', 'Изменить название команды {argInfoCommand, argInfo}', NEW.id),\n                ('/help', 'help', 'Получить список возможных команд {noArgs, argInfoCommand}', NEW.id);\n\n    -- Разрешения для ролей (admin, moderator, user)\n    INSERT INTO role_permissions (role_id, command_id)\n    SELECT r.id, c.id \n    FROM roles r, commands c \n    WHERE r.chat_id = NEW.id AND r.role_name = 'admin';\n\n    INSERT INTO role_permissions (role_id, command_id)\n    SELECT r.id, c.id \n    FROM roles r, commands c \n    WHERE r.chat_id = NEW.id AND r.role_name = 'moderator'\n    AND c.command IN ('/mute', '/kick', '/unmute', '/delete', '/start', '/info', '/help');\n\n    INSERT INTO role_permissions (role_id, command_id)\n    SELECT r.id, c.id \n    FROM roles r, commands c \n    WHERE r.chat_id = NEW.id AND r.role_name = 'user'\n    AND c.command IN ('/start', '/help', '/info');\n\n    RETURN NEW;\nEND;\n$$ LANGUAGE plpgsql"
    )
    op.replace_entity(public_insert_standard_roles_and_commands)

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    public_insert_standard_roles_and_commands = PGFunction(
        schema="public",
        signature="insert_standard_roles_and_commands()",
        definition="returns trigger\n LANGUAGE plpgsql\nAS $function$\nBEGIN\n    -- Вставляем стандартные роли\n    INSERT INTO roles (role_name, chat_id) VALUES \n        ('admin', NEW.id), \n        ('moderator', NEW.id), \n        ('user', NEW.id);\n    -- Вставляем стандартные команды\n    INSERT INTO commands (command, command_name, description, chat_id) VALUES \n                ('/start', 'start', 'Запустить бота', NEW.id),\n                ('/help', 'help', 'Получить помощь', NEW.id),\n                ('/mute', 'mute', 'Заглушить пользователя', NEW.id),\n                ('/kick', 'kick', 'Выгнать пользователя', NEW.id),\n                ('/unban', 'unban', 'Разбанить пользователя', NEW.id),\n                ('/delete', 'delete_message', 'Удалить сообщение пользователя', NEW.id),\n                ('/info', 'info', 'Информация о создателе', NEW.id),\n                ('/ban', 'ban', 'Забанить пользователя', NEW.id),\n                ('/unmute', 'unmute', 'Снять заглушение пользователя', NEW.id),\n                ('/chatSpamMuteTimeSet', 'chat_spam_mute_time_set', 'Установить время мута в чате', NEW.id),\n                ('/chatSpamNumMessageSet', 'chat_spam_num_message_set', 'Установить колличество сообщения для мута', NEW.id),\n                ('/chatSpamTimeSet', 'chat_spam_time_set', 'Установить время подсчитывания сообщений', NEW.id),\n                ('/chatdeletePatternSet', 'chat_delete_pattern_set', 'Установить паттерн удаляемых сообщений', NEW.id),\n                ('/roleAdd', 'role_add', 'Добавить роль', NEW.id),\n                ('/roleDelete', 'role_delete', 'Удалить роль', NEW.id),\n                ('/roleCommandAdd', 'role_command_add', 'Добавить команду для роли', NEW.id),\n                ('/roleCommandDelete', 'role_command_delete', 'Удалить команду для роли', NEW.id),\n                ('/userRoleSet', 'role_user_set', 'Устаноить пользователю роль', NEW.id),\n                ('/commandRename', 'command_rename', 'Изменить название команды', NEW.id),\n                ('/chatUser', 'chat_user', 'Получить информацию о юзере', NEW.id),\n                ('/chatStatsUserJoin', 'chat_stats_user_join', 'Получить статистику о подключившихся пользователях', NEW.id),\n                ('/chatStatsUserActive', 'chat_stats_user_active', 'Получить статистику активных пользователей', NEW.id),\n                ('/getCommandsRole', 'get_commands_role', 'Получить команды для роли', NEW.id);\n\n    -- Разрешения для ролей (admin, moderator, user)\n    INSERT INTO role_permissions (role_id, command_id)\n    SELECT r.id, c.id \n    FROM roles r, commands c \n    WHERE r.chat_id = NEW.id AND r.role_name = 'admin';\n\n    INSERT INTO role_permissions (role_id, command_id)\n    SELECT r.id, c.id \n    FROM roles r, commands c \n    WHERE r.chat_id = NEW.id AND r.role_name = 'moderator'\n    AND c.command IN ('/mute', '/kick', '/unmute', '/delete', '/start', '/info', '/help');\n\n    INSERT INTO role_permissions (role_id, command_id)\n    SELECT r.id, c.id \n    FROM roles r, commands c \n    WHERE r.chat_id = NEW.id AND r.role_name = 'user'\n    AND c.command IN ('/start', '/help', '/info');\n\n    RETURN NEW;\nEND;\n$function$"
    )
    op.replace_entity(public_insert_standard_roles_and_commands)
    # ### end Alembic commands ###
