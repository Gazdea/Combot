from aiogram import types
from db.Repository import ChatRepository, RoleRepository, UserRepository, MessageRepository, CommandRepository
from db.DTO import ChatDTO, RoleDTO, CommandDTO, UserDTO, MessageDTO 
from db.Mapper import Mapper
import re

class Handlers:
    def __init__(self, message: types.Message):
        # Получаем идентификаторы чата и пользователя
        chat_id = message.chat.id
        user_id = message.from_user.id
        
        # Инициализируем репозитории
        self.chat_repo = ChatRepository()
        self.user_repo = UserRepository()
        self.role_repo = RoleRepository()
        self.comd_repo = CommandRepository()

        # Получаем информацию о чате и пользователе
        self.chat = self.chat_repo.get_chat(chat_id)
        if not self.chat:
            self.chat_repo.create_chat(Mapper.chat_to_entity(ChatDTO(chat_id, message.chat.first_name)))
        self.user = self.user_repo.get_user(user_id)
        self.role = self.role_repo.get_role_user_form_chat(chat_id, user_id)
        self.command = self.comd_repo.get_commands_by_chat(chat_id)
        self.message = message
        
        mention_ids = [user.id for user in message.entities if user.type == 'mention']
        self.mention_users = self.user_repo.get_users(mention_ids) if mention_ids else None

    async def execute_command(self):
        """Выполняет команду, если она доступна пользователю."""
        command_name = self.message.text
        command_method = getattr(self, command_name, None)
        
        # Проверяем, существует ли команда
        if command_method:
            # Проверяем, есть ли у пользователя права на выполнение команды
            if self.role and command_name in self.role.allowed_commands:
                await command_method(self.message)
            else:
                await self.message.answer("У вас нет прав.")
        else:
            await self.message.answer("Команда не найдена.")  # Команда не существует

    # Остальные методы класса остаются без изменений
        
    async def info(self):
        """Вывод информации о боте для админа."""
        bot_info = """
    Этот бот позволяет модерировать чат.
    Разработан для упрощения администрирования.
    Создатель @Gazdea
            """
        await self.message.answer(bot_info)

    async def delete_message(self):
        """Удаляет сообщение из чата"""
        reply_to_message_id = self.message.reply_to_message.message_id
        if reply_to_message_id:
            try:
                await self.message.bot.delete_message(self.chat.id, self.message.message_id)
                await self.message.bot.delete_message(self.chat.id, reply_to_message_id)
            except Exception as e:
                await self.message.answer(f"Ошибка при удалении: {e}")


    async def kick(self):
        """Выгнать пользователя из чата"""
        if self.mention_users:
            try:
                for user in self.mention_users:
                    await self.message.bot.kick_chat_member(self.chat.id, user.id)
                await self.message.bot.delete_message(self.chat.id, self.message.message_id)
                await self.message.answer("Пользовател(ь/и) был выгнан(ы).")
            except Exception as e:
                await self.message.answer(f"Ошибка при выгоне: {e}")
        else:
            await self.message.answer("укажите @username.")


    async def mute(self, mute_time=3600):
        """Заглушить пользователя"""
        if self.mention_users:
            try:
                current_time = int(time.time())
                until_time = current_time + mute_time

                for user in self.mention_users:
                    await self.message.bot.restrict_chat_member(
                        self.chat.id, 
                        user.id, 
                        until_date=until_time, 
                        permissions=types.ChatPermissions(can_send_messages=False)
                    )
                await self.message.bot.delete_message(self.chat.id, self.message.message_id)
                await self.message.answer(f"Пользователь заглушен на {mute_time / 60:.1f} мин.")
                
                await asyncio.sleep(mute_time)
                # Снятие ограничения автоматически по истечении времени
                for user in self.mention_users:
                    await self.message.bot.restrict_chat_member(
                        self.chat.id, 
                        user.id, 
                        permissions=types.ChatPermissions(can_send_messages=True)
                    )
                await self.message.answer("Пользователь размьючен.")
                
            except Exception as e:
                await self.message.answer(f"Ошибка при муте: {e}")
        else:
            await self.message.answer("укажите @username.")


    async def unmute(self):
        """Снять мут с пользователя"""
        if self.mention_users:
            try:
                for user in self.mention_users:
                    await self.message.bot.restrict_chat_member(self.chat.id, user.id, permissions=types.ChatPermissions(can_send_messages=True))
                await self.message.bot.delete_message(self.chat.id, self.message.message_id)
                await self.message.answer("Мут снят.")
            except Exception as e:
                await self.message.answer(f"Ошибка при снятии мута: {e}")
        else:
            await self.message.answer("Ответьте на сообщение пользователя, с которого хотите снять мут.")


    async def ban(self):
        """Забанить пользователя"""
        if self.mention_users:
            try:
                for user in self.mention_users:
                    await self.message.bot.ban_chat_member(self.chat.id, user.id)
                await self.message.bot.delete_message(self.chat.id, self.message.message_id)
                await self.message.answer("Пользователь забанен.")
            except Exception as e:
                await self.message.answer(f"Ошибка при бане: {e}")
        else:
            await self.message.answer("Ответьте на сообщение пользователя, которого хотите забанить.")


    async def unban(self):
        """Разбанить пользователя"""
        if self.mention_users:
            try:
                for user in self.mention_users:
                    await self.message.bot.unban_chat_member(self.chat.id, user.id)
                await self.message.bot.delete_message(self.chat.id, self.message.message_id)
                await self.message.answer("Пользователь разбанен.")
            except Exception as e:
                await self.message.answer(f"Ошибка при разбане: {e}")
        else:
            await self.message.answer("Ответьте на сообщение пользователя, которого хотите разбанить.")


    async def anti_spam_protection(self, mute_time, max_messages, time_window):
        """Защита от спама: если пользователь отправляет больше max_messages за time_window секунд, он заглушается."""
        # Хранение времени отправки сообщений пользователями
        user_message_times = {}
        current_time = time.time()
        user_id = self.user.id
        # Инициализируем запись для пользователя, если её ещё нет
        if user_id not in user_message_times:
            user_message_times[user_id] = []

        # Убираем устаревшие записи, которые вышли за пределы временного окна
        user_message_times[user_id] = [timestamp for timestamp in user_message_times[user_id] if current_time - timestamp < time_window]

        # Добавляем текущее время отправки сообщения
        user_message_times[user_id].append(current_time)

        # Если сообщений больше, чем разрешено, заглушаем пользователя
        if len(user_message_times[user_id]) > max_messages:
            self.message.text = self.message.from_user.id
            await self.mute(mute_time)
            return True
        return False

    async def remove_links(self):
        """Удаляет сообщения, содержащие ссылки."""
        # Регулярное выражение для обнаружения ссылок
        LINK_REGEX = r"(https?://[^\s]+)"
        
        if re.search(LINK_REGEX, self.message.text):
            try:
                await self.message.bot.delete_message(self.chat.id, self.message.message_id)
                await self.message.answer("Сообщения с ссылками запрещены.")
            except Exception as e:
                await self.message.answer(f"Ошибка при удалении сообщения с ссылкой: {e}")
                
    async def welcome_new_member(self):
        for new_user in self.message.new_chat_members:
            if new_user.id == self.message.bot.id:
                chat_id = self.message.chat.id
                chat_name = self.message.chat.first_name
                await self.message.bot.send_message(chat_id, "Бот добавлен в этот чат! Привет!")
                members = await self.message.bot.get_chat_administrators(chat_id)
                self.chat_repo.create_chat(ChatDTO(chat_id=chat_id, chat_name=chat_name))
                for member in members:
                    self.user_repo.create_user(UserDTO(id=member.user.id, username=member.user.first_name, join_date=datetime.datetime.now()))
            else:
                self.user_repo.create_user(UserDTO(id=new_user.id, username=new_user.first_name, join_date=datetime.datetime.now()))
                welcome_text = f"Привет, {new_user.first_name}! Добро пожаловать в наш чат."
                await self.message.bot.send_message(self.chat.id, welcome_text)