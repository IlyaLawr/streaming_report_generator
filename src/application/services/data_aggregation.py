from asyncio import gather

from application.interface.file_reader import IFileReader
from application.interface.temp_storage import ITempStorage


class DataAggregationService:
    def __init__(self,
                 file_reader: IFileReader,
                 temp_storage: ITempStorage,
                 delimiter_csv: str = ',') -> None:

        self._file_reader = file_reader
        self._temp_storage= temp_storage
        self._delimiter = delimiter_csv


    async def aggregate(self, file_paths: list[str]) -> bool | None:
        async with self._temp_storage as temp_storage:
            await gather(
                *(self._process_file(path, temp_storage) for path in file_paths)
            )
        return True


    async def _process_file(self, path: str, temp_storage) -> None:
   
        lines = self._file_reader.read(path)
        headers = (await anext(lines)).split(self._delimiter)
        async for line in lines:
            data = self._parse_line(headers, line)
            await temp_storage.write(data)


    def _parse_line(self, headers: list[str], line: str) -> dict:
        data = {}
        for headers, value in zip(headers, line.split(self._delimiter)):
            data[headers] = value
        return data
