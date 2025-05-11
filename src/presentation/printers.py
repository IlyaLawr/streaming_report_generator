from __future__ import annotations
from typing import Any, Optional, Type
from types import TracebackType

from application.interface.report_writer import IReportWriter
from presentation.formatters import IReportFormatter


class ConsoleWriter(IReportWriter):
    def __init__(self, formatter: IReportFormatter) -> None:
        self._formatter = formatter


    async def __aenter__(self) -> ConsoleWriter:
        return self


    async def __aexit__(self,
                        exc_type: Optional[Type[BaseException]],
                        exc_value: Optional[BaseException],
                        tb: Optional[TracebackType]) -> None:
        await self.close()


    async def write_part(self, data: dict[str, Any]) -> None:
        formatted_report = self._formatter.format_report(data)
        print(formatted_report)


    async def close(self) -> None:
        pass
