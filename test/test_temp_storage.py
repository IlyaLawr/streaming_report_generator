from json import loads
from os import remove

from pytest import mark
from aiosqlite import connect

from infrastructure.sqlite_storage import SQLTempStorage


@mark.asyncio
async def test_temp_storage_write():
    db_path = 'test.db'

    temp_storage = SQLTempStorage(db_path, 'temp')

    async with temp_storage as temp_storage:

        await temp_storage.write({'department': 'A', 'value': 1})
        await temp_storage.write({'department': 'B', 'value': 2})
        await temp_storage.write({'department': 'C', 'value': 3})

    async with connect(db_path) as conn:
        result = await conn.execute('SELECT data FROM temp')
        rows = [row[0] for row in await result.fetchall()]

    objs = [loads(r) for r in rows]

    assert len(objs) == 3
    assert {'department': 'A', 'value': 1} in objs
    assert {'department': 'B', 'value': 2} in objs
    assert {'department': 'C', 'value': 3} in objs

    remove(db_path)



@mark.asyncio
async def test_temp_storage_read_sorted():
    db_path = 'test.db'

    temp_storage = SQLTempStorage(db_path, 'temp')

    async with temp_storage as temp_storage:
        await temp_storage.write({'department': 'B', 'value': 5})
        await temp_storage.write({'department': 'A', 'value': 1})
        await temp_storage.write({'department': 'C', 'value': 7})
        await temp_storage.write({'department': 'B', 'value': 2})
        await temp_storage.write({'department': 'A', 'value': 3})

    result = []

    async for data in temp_storage.read(group_by='department'):
        result.append(data)

    assert all(data['department'] == 'A' for data in result[:2])
    assert all(data['department'] == 'B' for data in result[2:4])
    assert all(data['department'] == 'C' for data in result[5:])

    remove(db_path)
