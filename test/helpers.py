import pytest
from httpx import AsyncClient


def generate_authorization_header(access_token: str) -> dict:
    return {"Authorization": f"Bearer {access_token}"}


async def get_access_token(client: AsyncClient, email: str = "email@example.com") -> str:
    await client.post(
        "/users",
        json={
            "email": email,
            "password": "String123",
            "full_name": "Minh Hoang",
        },
    )
    response = await client.post(
        "/users/auth",
        json={
            "email": email,
            "password": "String123",
        },
    )
    return response.json().get("access_token")


@pytest.fixture
async def access_token(client: AsyncClient) -> str:
    return await get_access_token(client)


@pytest.fixture
async def access_token_other_user(client: AsyncClient) -> str:
    return await get_access_token(client, "other@email.com")


@pytest.fixture
async def category_creation(client: AsyncClient, access_token: str) -> None:
    await client.post(
        "/categories",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"name": "Car", "description": "Car has 4 wheels"},
    )


@pytest.fixture
async def item_creation(
    client: AsyncClient,
    access_token: str,
    category_creation,
) -> None:
    await client.post(
        "/categories/1/items",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "name": "Volvo",
            "description": "Volvo from Germany",
        },
    )


@pytest.fixture
async def list_items_creation(
    client: AsyncClient,
    access_token: str,
    category_creation,
):
    # Create 30 items to add to category
    for time in range(30):
        await client.post(
            "/categories/1/items",
            headers={"Authorization": f"Bearer {access_token}"},
            json={"name": "Volvo" + str(time), "description": "Volvo from Germany"},
        )
