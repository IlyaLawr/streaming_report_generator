from os import remove

from pytest import mark
from aiofiles import open

from infrastructure.csv_file_reader import AiofilesAsyncFileReader


@mark.asyncio
async def test_filereader_reads_lines():
    file_path = 'test.csv'

    lines = [['a', 'b', 'c', '1'],
             ['a1', 'b1', 'c1', '11'],
             ['a2', 'b2', 'c2', '12'],
             ['a3', 'b3', 'c3', '13'] 
             ]

    async with open(file_path, "w") as file:
        for line in lines:
            await file.write(','.join(line) + '\n')

    reader = AiofilesAsyncFileReader()
    result = []

    async for line in reader.read(file_path):
        result.append(line.split(','))

    assert result == lines
    remove(file_path)
