from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, AsyncIterator, Optional, Type
from types import TracebackType


class ITempStorage(ABC):
    """Интерфейс для асинхронного временного хранилища данных."""

    @abstractmethod
    async def __aenter__(self) -> ITempStorage:
        pass


    @abstractmethod
    async def __aexit__(self,
                        exc_type: Optional[Type[BaseException]],
                        exc_value: Optional[BaseException],
                        tb: Optional[TracebackType]) -> None:
        pass


    @abstractmethod
    async def write(self, data: dict[str, Any]) -> None:
        """
        Добавить одну запись в буфер хранилища.
        При достижении порога буфера должны автоматически сохраняться данные.
        :param data: произвольный словарь данных для хранения
        """
        pass


    @abstractmethod
    async def read(self, group_by: str) -> AsyncIterator[dict[str, Any]]:
        """
        Прочитать все записи, отсортированные по ключу внутри храналища.
        :param group_by: имя поля для сортировки
        :return: асинхронный итератор словарей с данными
        """
        pass


    @abstractmethod
    async def close(self) -> None:
        pass
