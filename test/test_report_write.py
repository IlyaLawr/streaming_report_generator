from pytest import mark
from aiofiles import open

from json import loads
from os import remove

from infrastructure.json_file_write import JSONWriter


parts = [
        [{'A': {'x': 1}, '1': 11},
        {'B': {'y': 2}, '2': 22},
        {'C': {'z': 3}, '3': 33},
        {'D': {'j': 4}, '4': 44}],

        [{'A': {'x': 1}, '1': 11},
        {'B': {'y': 2}, '2': 22},
        {'C': {'z': 3}, '3': 33},
        {'D': {'j': 4}, '4': 44},
        {'F': {'k': 5}, '4': 55}],

        [{'0': {'a': 0}, 0: -0}]
]


@mark.asyncio
@mark.parametrize('part', [(parts[0]), 
                           (parts[1]),
                           (parts[2])]
)
async def test_report_write(part):
    file_path = 'test.json'

    parts = [
        {'A': {'x': 1}, '1': 11},
        {'B': {'y': 2}, '2': 22},
        {'C': {'z': 3}, '3': 33},
        {'D': {'j': 4}, '4': 44},
    ]

    writer = JSONWriter(file_path)

    async with writer:
        for part in parts:
            await writer.write_part(part)


    async with open(file_path, "r", encoding="utf-8") as file:
        data = await file.read()

    data = loads(data)

    assert isinstance(data, list)
    assert data == parts

    remove(file_path)
