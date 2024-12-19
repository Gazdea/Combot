from abc import ABC, abstractmethod
from typing import Any, List


class UtilBot(ABC):
    
    @abstractmethod
    def list_to_string(self, list_str: List[Any], start_str: str = "", end_str: str = "", intermediate_str: str = "") -> str:
        raise NotImplementedError