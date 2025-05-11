from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Optional, Type
from types import TracebackType


class IReportWriter(ABC):
    """Интерфейс для асинхронной записи «партии» данных отчёта."""

    @abstractmethod
    async def __aenter__(self) -> IReportWriter:
        pass


    @abstractmethod
    async def __aexit__(self,
                        exc_type: Optional[Type[BaseException]],
                        exc_value: Optional[BaseException],
                        tb: Optional[TracebackType]) -> None:
        pass


    @abstractmethod
    async def write_part(self, data: dict[str, Any]) -> None:
        """
        Записать одну «партию» данных.
        :param data: словарь с данными
        """
        pass


    @abstractmethod
    async def close(self) -> None:
        pass
