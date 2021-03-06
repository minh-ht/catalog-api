from test.helpers import generate_authorization_header
from typing import Union

import pytest
from fastapi import status
from httpx import AsyncClient


async def test_fail_to_create_category_without_authentication(client: AsyncClient):
    response = await client.post(
        "/categories",
        json={
            "name": "Car",
            "description": "Car has 4 wheels",
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"error_message": "User needs to authenticate"}


@pytest.mark.parametrize(
    "category_data, expected_json_response",
    [
        # Name length is less than 1
        (
            {
                "name": "",
                "description": "Car has 4 wheels",
            },
            {"error_message": "name: ensure this value has at least 1 characters"},
        ),
        # Name length is greater than 50
        (
            {
                "name": "Car" + "r" * 50,
                "description": "Car has 4 wheels",
            },
            {"error_message": "name: ensure this value has at most 50 characters"},
        ),
        # Name length is 51
        (
            {
                "name": "C" * 51,
                "description": "A lot of C",
            },
            {"error_message": "name: ensure this value has at most 50 characters"},
        ),
    ],
)
async def test_fail_to_create_category_with_invalid_name(
    client: AsyncClient,
    access_token: str,
    category_data: dict,
    expected_json_response: dict,
):
    response = await client.post(
        "/categories",
        headers=generate_authorization_header(access_token),
        json=category_data,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == expected_json_response


@pytest.mark.parametrize(
    "category_data, expected_json_response",
    [
        # Description length is less than 1
        (
            {
                "name": "Car",
                "description": "",
            },
            {"error_message": "description: ensure this value has at least 1 characters"},
        ),
        # Description length is greater than 50
        (
            {
                "name": "Car",
                "description": "Car has 4 wheels" + "s" * 5000,
            },
            {"error_message": "description: ensure this value has at most 5000 characters"},
        ),
        # Description length is 5001
        (
            {
                "name": "Car",
                "description": "s" * 5001,
            },
            {"error_message": "description: ensure this value has at most 5000 characters"},
        ),
    ],
)
async def test_fail_to_create_category_with_invalid_description(
    client: AsyncClient,
    access_token: str,
    category_data: dict,
    expected_json_response: dict,
):
    response = await client.post(
        "/categories",
        headers=generate_authorization_header(access_token),
        json=category_data,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == expected_json_response


async def test_fail_to_create_category_with_existing_name(client: AsyncClient, access_token: str):
    category_data = {
        "name": "Car",
        "description": "Car has 4 wheels",
    }
    await client.post(
        "/categories",
        headers=generate_authorization_header(access_token),
        json=category_data,
    )
    response = await client.post(
        "/categories",
        headers=generate_authorization_header(access_token),
        json=category_data,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"error_message": "Category already exists"}


async def test_create_category_successfully(client: AsyncClient, access_token: str):
    response = await client.post(
        "/categories",
        headers=generate_authorization_header(access_token),
        json={
            "name": "Car",
            "description": "Car has 4 wheels",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {"id": 1}

    # Test if category is created on the server
    response = await client.get("/categories/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "name": "Car",
        "description": "Car has 4 wheels",
    }


async def test_get_categories_successfully(client: AsyncClient, access_token: str):
    # Create categories
    for name_postfix in range(2):
        await client.post(
            "/categories",
            headers=generate_authorization_header(access_token),
            json={
                "name": "Car " + str(name_postfix),
                "description": "Car has 4 wheels",
            },
        )
    # Get categories
    response = await client.get("/categories")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {"id": 1, "name": "Car 0"},
        {"id": 2, "name": "Car 1"},
    ]


@pytest.mark.parametrize(
    "category_id, expected_status_code, expected_json_response",
    [
        # Category id is invalid
        (
            "a",
            status.HTTP_400_BAD_REQUEST,
            {"error_message": "category_id: value is not a valid integer"},
        ),
        # Category id does not exist
        (
            10,
            status.HTTP_404_NOT_FOUND,
            {"error_message": "Cannot find the specified category"},
        ),
    ],
)
async def test_fail_to_get_single_category(
    client: AsyncClient,
    category_creation: None,
    category_id: Union[int, str],
    expected_status_code: int,
    expected_json_response: dict,
):
    response = await client.get(f"/categories/{category_id}")
    assert response.status_code == expected_status_code
    assert response.json() == expected_json_response


async def test_get_single_category_successfully(client: AsyncClient, category_creation: None):
    response = await client.get("/categories/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "name": "Car",
        "description": "Car has 4 wheels",
    }


async def test_fail_to_delete_category_without_authentication(client: AsyncClient, category_creation: None):
    response = await client.delete("/categories/1")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"error_message": "User needs to authenticate"}


async def test_fail_to_delete_category_not_without_ownership(
    client: AsyncClient,
    access_token: str,
    category_creation: None,
    access_token_other_user: str,
):
    # Other user tries to delete category
    response = await client.delete(
        "/categories/1",
        headers=generate_authorization_header(access_token_other_user),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"error_message": "User does not have permission to perform this action"}


async def test_fail_to_delete_category_with_non_existent_category(
    client: AsyncClient,
    access_token: str,
    category_creation: None,
):
    response = await client.delete(
        "/categories/10",
        headers=generate_authorization_header(access_token),
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"error_message": "Cannot find the specified category"}


async def test_fail_to_delete_category_with_invalid_category_id(
    client: AsyncClient,
    access_token: str,
    category_creation: None,
):
    response = await client.delete(
        "/categories/a",
        headers=generate_authorization_header(access_token),
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"error_message": "category_id: value is not a valid integer"}


async def test_delete_category_successfully(
    client: AsyncClient,
    access_token: str,
    category_creation: None,
):
    response = await client.delete(
        "/categories/1",
        headers=generate_authorization_header(access_token),
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {}

    # Test if category is deleted on the server
    response = await client.get("/categories/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"error_message": "Cannot find the specified category"}
