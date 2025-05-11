from __future__ import annotations
from typing import AsyncIterator, Any, Optional, Type
from types import TracebackType
from json import loads, dumps

from aiosqlite import connect

from application.interface.temp_storage import ITempStorage


class SQLTempStorage(ITempStorage):
    def __init__(self, db_path: str, table: str) -> None:
        self._table = table
        self._db_path = db_path
        self._buffer = []
        self._buffer_size = 20
        self._table_is_read = False


    async def __aenter__(self) -> SQLTempStorage:
        await self._create_table()
        return self


    async def __aexit__(self,
                        exc_type: Optional[Type[BaseException]],
                        exc_value: Optional[BaseException],
                        tb: Optional[TracebackType]) -> None:
        await self.close()


    async def write(self, data: dict[str, Any]) -> None:
        self._buffer.append(data)
        if len(self._buffer) > self._buffer_size:
            await self._flush_buffer()


    async def _flush_buffer(self) -> None:
        query = f'INSERT INTO {self._table}(data) VALUES (?)'
        params = [(dumps(data), ) for data in self._buffer]
        async with connect(self._db_path) as conn:
            await conn.executemany(query, params)
            await conn.commit()
        self._buffer.clear()


    async def read(self, group_by: str) -> AsyncIterator[dict[str, Any]]:

        order = f'ORDER BY json_extract(data, "$.{group_by}")'
        query = f'SELECT data FROM {self._table} {order}'

        async with connect(self._db_path) as conn:
            cursor = await conn.execute(query)
            async for row in cursor:
                yield loads(row[0])

            self._table_is_read = True


    async def _create_table(self) -> None:
        async with connect(self._db_path) as conn:
            await conn.execute(
                f'''
                CREATE TABLE IF NOT EXISTS {self._table} (
                    id INTEGER PRIMARY KEY,
                    data JSON NOT NULL
                )
                '''
            )
            await conn.commit()


    async def close(self) -> None:
        if self._table_is_read:
            async with connect(self._db_path) as conn:
                await conn.execute(f'DROP TABLE {self._table}')
                await conn.commit()
        else:
            if self._buffer:
                await self._flush_buffer()
