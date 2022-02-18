import asyncio.unix_events

import pytest
from httpx import AsyncClient

from main.main import app
from main.services import session

pytest_plugins = ["test.helpers"]


@pytest.fixture(scope="session")
def event_loop() -> any:
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function", autouse=True)
async def connection() -> None:
    async with session.engine.begin() as connection:
        await connection.run_sync(session.Base.metadata.drop_all)
        await connection.run_sync(session.Base.metadata.create_all)


@pytest.fixture
async def client() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as test_client:
        yield test_client
