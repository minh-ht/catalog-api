from test.helpers import generate_authorization_header
from typing import Union

import pytest
from fastapi import status
from httpx import AsyncClient


async def test_fail_to_create_item_unauthenticated(client: AsyncClient, create_item: None):
    response = await client.post(
        "/categories/1/items",
        json={
            "name": "Volvo",
            "description": "Volvo from Germany",
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"error_message": "User needs to authenticate"}


@pytest.mark.parametrize(
    "item_data, expected_json_response",
    [
        # Name length is less than 1
        (
            {
                "name": "",
                "description": "Volvo from Germany",
            },
            {"error_message": "ensure this value has at least 1 characters"},
        ),
        # Name length is greater than 50
        (
            {
                "name": "Volvo" + "o" * 50,
                "description": "Volvo from Germany",
            },
            {"error_message": "ensure this value has at most 50 characters"},
        ),
        # Name length is 51
        (
            {
                "name": "V" * 51,
                "description": "A lot of V",
            },
            {"error_message": "ensure this value has at most 50 characters"},
        ),
    ],
)
async def test_fail_to_create_item_with_invalid_name(
    client: AsyncClient,
    access_token: str,
    create_category: None,
    item_data: dict,
    expected_json_response: dict,
):
    response = await client.post(
        "/categories/1/items",
        headers=generate_authorization_header(access_token),
        json=item_data,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == expected_json_response


@pytest.mark.parametrize(
    "item_data, expected_json_response",
    [
        # Description length is less than 1
        (
            {
                "name": "Volvo",
                "description": "",
            },
            {"error_message": "ensure this value has at least 1 characters"},
        ),
        # Description length is greater than 50
        (
            {
                "name": "Volvo",
                "description": "Volvo from Germany" + "s" * 5000,
            },
            {"error_message": "ensure this value has at most 5000 characters"},
        ),
        # Description length 5001
        (
            {
                "name": "Volvo",
                "description": "V" * 5001,
            },
            {"error_message": "ensure this value has at most 5000 characters"},
        ),
    ],
)
async def test_fail_to_create_item_with_invalid_description(
    client: AsyncClient,
    access_token: str,
    create_category: None,
    item_data: dict,
    expected_json_response: dict,
):
    response = await client.post(
        "/categories/1/items",
        headers=generate_authorization_header(access_token),
        json=item_data,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == expected_json_response


async def test_fail_to_create_item_with_existed_name(
    client: AsyncClient,
    access_token: str,
    create_category: None,
):
    item_data = {
        "name": "Volvo",
        "description": "Volvo from Germany",
    }
    await client.post(
        "/categories/1/items",
        headers=generate_authorization_header(access_token),
        json=item_data,
    )
    response = await client.post(
        "/categories/1/items",
        headers=generate_authorization_header(access_token),
        json=item_data,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"error_message": "Item already exists"}


async def test_create_item_successfully(
    client: AsyncClient,
    access_token: str,
    create_category: None,
):
    response = await client.post(
        "/categories/1/items",
        headers=generate_authorization_header(access_token),
        json={
            "name": "Volvo",
            "description": "Volvo from Germany",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {}


@pytest.mark.parametrize(
    "page, items_per_page, expected_json_response",
    [
        # Page is not greater than 0
        (
            0,
            10,
            {"error_message": "ensure this value is greater than 0"},
        ),
        # Items_per_page is not greater than 0
        (
            1,
            0,
            {"error_message": "ensure this value is greater than 0"},
        ),
        # Page is not an integer
        (
            "a",
            10,
            {"error_message": "value is not a valid integer"},
        ),
        # Items_per_page is not an integer
        (
            5,
            "a",
            {"error_message": "value is not a valid integer"},
        ),
    ],
)
async def test_fail_get_items_with_invalid_query_parameter(
    client: AsyncClient,
    create_many_items: None,
    page: int,
    items_per_page: int,
    expected_json_response: dict,
):
    response = await client.get(f"/categories/1/items?page={page}&items_per_page={items_per_page}")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == expected_json_response


@pytest.mark.parametrize(
    "page, items_per_page, expected_json_response_list_length",
    [
        (2, 5, 5),
        (10, 3, 3),
        (11, 3, 0),
        (4, 9, 3),
        (10, 5, 0),
    ],
)
async def test_get_items_successfully(
    client: AsyncClient,
    create_many_items: None,
    page: int,
    items_per_page: int,
    expected_json_response_list_length: dict,
):
    response = await client.get(f"/categories/1/items?page={page}&items_per_page={items_per_page}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == expected_json_response_list_length


async def test_get_items_successfully_with_default_value(client: AsyncClient, create_many_items: None):
    response = await client.get("/categories/1/items")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 20


@pytest.mark.parametrize(
    "item_id, expected_status_code, expected_json_response",
    [
        # Item id is invalid
        (
            "a",
            status.HTTP_400_BAD_REQUEST,
            {"error_message": "value is not a valid integer"},
        ),
        # Item id does not exist
        (
            10,
            status.HTTP_404_NOT_FOUND,
            {"error_message": "Cannot find the specified item"},
        ),
    ],
)
async def test_fail_to_get_single_item(
    client: AsyncClient,
    create_item: None,
    item_id: Union[int, str],
    expected_status_code: int,
    expected_json_response: dict,
):
    response = await client.get(f"/categories/1/items/{item_id}")
    assert response.status_code == expected_status_code
    assert response.json() == expected_json_response


async def test_get_single_item_successfully(client: AsyncClient, create_item: None):
    response = await client.get("/categories/1/items/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"name": "Volvo", "description": "Volvo from Germany"}


async def test_fail_to_delete_item_unauthenticated(
    client: AsyncClient,
    access_token: str,
    create_item: None,
):
    response = await client.delete("/categories/1/items/1")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"error_message": "User needs to authenticate"}


async def test_fail_to_delete_item_not_owner(
    client: AsyncClient,
    access_token: str,
    access_token_other_user: str,
    create_item: None,
):
    # Other user tries to delete item
    response = await client.delete(
        "/categories/1",
        headers=generate_authorization_header(access_token_other_user),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"error_message": "User does not have permission to perform this action"}


async def test_fail_to_delete_item_not_found(
    client: AsyncClient,
    access_token: str,
    create_item: None,
):
    response = await client.delete(
        "/categories/1/items/10",
        headers=generate_authorization_header(access_token),
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"error_message": "Cannot find the specified item"}


async def test_fail_to_delete_item_with_invalid_item_id(
    client: AsyncClient,
    access_token: str,
    create_item: None,
):
    response = await client.delete(
        "/categories/1/items/a",
        headers=generate_authorization_header(access_token),
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"error_message": "value is not a valid integer"}


async def test_delete_item_successfully(
    client: AsyncClient,
    access_token: str,
    create_item: None,
):
    response = await client.delete(
        "/categories/1/items/1",
        headers=generate_authorization_header(access_token),
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {}
