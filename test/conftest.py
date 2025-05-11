from pytest import fixture
from unittest.mock import AsyncMock

from infrastructure.sqlite_storage import SQLTempStorage
from infrastructure.json_file_write import JSONWriter


@fixture
def mock_temp_storage():
    mock = AsyncMock(spec=SQLTempStorage)
    mock.__aenter__.return_value = mock
    mock.__aexit__.return_value = None
    return mock


@fixture
def mock_report_writer():
    mock = AsyncMock(spec=JSONWriter)
    mock.__aenter__.return_value = mock
    mock.__aexit__.return_value = None
    return mock