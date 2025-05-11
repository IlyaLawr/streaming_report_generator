from typing import AsyncIterator

from aiofiles import open

from application.interface.file_reader import IFileReader


class AiofilesAsyncFileReader(IFileReader):
    async def read(self, path: str) -> AsyncIterator[str]:
        try:
            async with open(path, mode='r', encoding='utf-8') as f:
                async for raw in f:
                    yield raw.rstrip('\n')
        except:
            raise ValueError(f'Не удалось прочитать файл по пути "{path}", проверьте наличие файла и повторите попытку.')
