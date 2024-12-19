from typing import Any, List

from app.bot.util.UtilBot import UtilBot


class UtilBotImpl(UtilBot):
    
    def list_to_string(self, list_str: List[Any], start_str: str = "", end_str: str = "", intermediate_str: str = ", ") -> str:
        response = [start_str] if start_str else []
        response.append(intermediate_str.join(map(str, list_str)))
        if end_str:
            response.append(end_str)
        return "\n".join(response)