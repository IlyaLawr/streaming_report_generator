from abc import ABC, abstractmethod
from typing import AsyncIterator


class IFileReader(ABC):
    """Интерфейс для асинхронного построчного чтения файлов."""

    @abstractmethod
    async def read(self, path: str) -> AsyncIterator[str]:
        """
        Открывает файл и выдаёт строки без символа перевода строки.

        :param path: путь к файлу
        :return: асинхронный генератор строк
        :raises ValueError: если файл недоступен для чтения
        """
        pass
