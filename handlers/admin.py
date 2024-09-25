from db.connection import add_user, remove_user, get_user_role

def handle_start(bot, message):
    """Приветствие для админа."""
    bot.send_message(message.chat.id, "Привет, админ! Что хотите сделать?")

def handle_add_moderator(bot, message):
    """Добавление модератора по ID пользователя."""
    try:
        user_id = int(message.text.split()[1])  # Ожидается, что пользователь введет команду в формате /add_moderator <user_id>
        add_user(user_id, username=None, chat_id=None, role_name="moderator")
        bot.send_message(message.chat.id, f"Пользователь {user_id} теперь модератор.")
    except (IndexError, ValueError):
        bot.send_message(message.chat.id, "Используйте правильный формат команды: /add_moderator <user_id>")

def handle_remove_user(bot, message):
    """Удаление пользователя по ID."""
    try:
        user_id = int(message.text.split()[1])  # Ожидается, что админ введет команду в формате /remove_user <user_id>
        if remove_user(user_id):
            bot.send_message(message.chat.id, f"Пользователь {user_id} удален.")
        else:
            bot.send_message(message.chat.id, f"Пользователь {user_id} не найден.")
    except (IndexError, ValueError):
        bot.send_message(message.chat.id, "Используйте правильный формат команды: /remove_user <user_id>")
