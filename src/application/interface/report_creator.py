from abc import ABC, abstractmethod
from typing import Coroutine


class IReportCreator(ABC):
    """
    Интерфейс для классов, формирующих и записывающих отчёт.
    """

    @abstractmethod
    def create(self) -> Coroutine[None, None, None]:
        """
        Запустить сбор, агрегацию и запись отчёта.

        Возвращает корутину, которая при выполнении:
          1. Считывает данные из ITempStorage (группируя по нужному ключу).
          2. Обрабатывает их (парсит, считает итоги по отделам и т.п.).
          3. Пишет «партии» результатов в IReportWriter.

        :raises ValueError: при некорректном формате данных
        """
        pass
