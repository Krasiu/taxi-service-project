from pathlib import Path
from typing import AsyncGenerator

import pytest

from dispatch_service.dal.database import database
from dispatch_service.dal.migrate import create_tables


@pytest.fixture(scope="session", autouse=True)
def create_database_tables() -> None:
    create_tables()


@pytest.fixture(scope="session", autouse=True)
async def database_connection() -> AsyncGenerator[None, None]:
    await database.connect()
    yield database
    await database.disconnect()
    Path("test.db").unlink(missing_ok=True)
