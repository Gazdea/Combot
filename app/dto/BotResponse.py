from typing import Optional, Dict

class BotResponse:
    def __init__(self, 
                 text: str, 
                 reply_markup: Optional[Dict[str, str]] = None, 
                 media: Optional[Dict[str, str]] = None, 
                 parse_mode: Optional[str] = "Markdown", 
                 timeout: Optional[int] = None, 
                 disable_notification: bool = False):
        """
        Представляет ответ бота.

        :param text: Текст ответа, который будет отправлен пользователю.
        :param reply_markup: Дополнительные элементы управления, такие как клавиатура.
        :param media: Медиафайлы, которые могут быть отправлены вместе с текстом.
        :param parse_mode: Режим обработки текста (например, Markdown или HTML).
        :param timeout: Время ожидания в секундах.
        :param disable_notification: Если True, сообщение будет отправлено без уведомления.
        """
        self.text = text
        self.reply_markup = reply_markup
        self.media = media
        self.parse_mode = parse_mode
        self.timeout = timeout
        self.disable_notification = disable_notification

    def __repr__(self) -> str:
        return f"BotResponse(text={self.text}, reply_markup={self.reply_markup}, media={self.media}, " \
               f"parse_mode={self.parse_mode}, timeout={self.timeout}, disable_notification={self.disable_notification})"
