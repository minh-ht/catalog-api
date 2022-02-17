import asyncio

import pytest
from httpx import AsyncClient

from main.main import app
from main.services import session


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function", autouse=True)
async def connection() -> None:
    async with session.engine.begin() as connection:
        await connection.run_sync(session.Base.metadata.drop_all)
        await connection.run_sync(session.Base.metadata.create_all)


@pytest.fixture()
async def client() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as test_client:
        yield test_client


@pytest.fixture()
async def access_token(client: AsyncClient) -> str:
    await client.post(
        "/users", json={"email": "email0@example.com", "password": "String123", "full_name": "Minh Hoang"}
    )
    response = await client.post(
        "/users/auth",
        json={
            "email": "email0@example.com",
            "password": "String123",
        },
    )
    return response.json().get("access_token")


@pytest.fixture()
async def access_token_other_user(client: AsyncClient) -> str:
    await client.post(
        "/users", json={"email": "email_other@example.com", "password": "String123", "full_name": "Minh Hoang"}
    )
    response = await client.post(
        "/users/auth",
        json={
            "email": "email_other@example.com",
            "password": "String123",
        },
    )
    return response.json().get("access_token")


@pytest.fixture()
async def create_category(client: AsyncClient, access_token: str) -> None:
    await client.post(
        "/categories",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"name": "Car", "description": "Car has 4 wheels"},
    )


@pytest.fixture()
async def create_item(
    client: AsyncClient,
    access_token: str,
    create_category: None,
) -> None:
    await client.post(
        "/categories/1/items",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "name": "Volvo",
            "description": "Volvo from Germany",
        },
    )


@pytest.fixture()
async def create_many_items(
    client: AsyncClient,
    access_token: str,
    create_category: None,
):
    # Create 30 items to add to category
    for time in range(30):
        await client.post(
            "/categories/1/items",
            headers={"Authorization": f"Bearer {access_token}"},
            json={"name": "Volvo" + str(time), "description": "Volvo from Germany"},
        )
