from __future__ import annotations
from typing import Any, Optional, Type
from types import TracebackType
from json import dumps

from aiofiles import open

from application.interface.report_writer import IReportWriter


class JSONWriter(IReportWriter):
    def __init__(self, path: str) -> None:
        self._path = path
        self._encoding = 'utf-8'
        self._buffer_size = 100
        self._buffer = []
        self._file = None


    async def __aenter__(self):
        self._file = await open(self._path, mode='w', encoding=self._encoding)
        await self._file.write('[')
        return self


    async def __aexit__(self,
                        exc_type: Optional[Type[BaseException]],
                        exc_value: Optional[BaseException],
                        tb: Optional[TracebackType]) -> None:
        await self.close()


    async def write_part(self, data: dict[str, Any]):
        self._buffer.append(data)

        if len(self._buffer) >= self._buffer_size:
            await self._flush_buffer()
            
    
    async def _flush_buffer(self):
        if not self._buffer or not self._file:
            return
        
        lines = []

        for data in self._buffer:
            line = dumps(data, ensure_ascii=False, indent=2)
            lines.append(line)
            
        await self._file.write(',\n'.join(lines))
        self._buffer.clear()

  
    async def close(self):
        if not self._file:
            return

        await self._flush_buffer()
        await self._file.write(']')
        await self._file.close()

        self._file = None
