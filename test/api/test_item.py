from test.helpers import generate_authorization_header
from typing import Union

import pytest
from fastapi import status
from httpx import AsyncClient


async def test_fail_to_create_item_without_authentication(client: AsyncClient, item_creation: None):
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
            {"error_message": "name: ensure this value has at least 1 characters"},
        ),
        # Name length is greater than 50
        (
            {
                "name": "Volvo" + "o" * 50,
                "description": "Volvo from Germany",
            },
            {"error_message": "name: ensure this value has at most 50 characters"},
        ),
        # Name length is 51
        (
            {
                "name": "V" * 51,
                "description": "A lot of V",
            },
            {"error_message": "name: ensure this value has at most 50 characters"},
        ),
    ],
)
async def test_fail_to_create_item_with_invalid_name(
    client: AsyncClient,
    access_token: str,
    category_creation: None,
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
            {"error_message": "description: ensure this value has at least 1 characters"},
        ),
        # Description length is greater than 50
        (
            {
                "name": "Volvo",
                "description": "Volvo from Germany" + "s" * 5000,
            },
            {"error_message": "description: ensure this value has at most 5000 characters"},
        ),
        # Description length 5001
        (
            {
                "name": "Volvo",
                "description": "V" * 5001,
            },
            {"error_message": "description: ensure this value has at most 5000 characters"},
        ),
    ],
)
async def test_fail_to_create_item_with_invalid_description(
    client: AsyncClient,
    access_token: str,
    category_creation: None,
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


async def test_fail_to_create_item_with_existing_name(
    client: AsyncClient,
    access_token: str,
    category_creation: None,
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
    category_creation: None,
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
    assert response.json() == {"id": 1}

    # Test if item is created on the server
    response = await client.get("/categories/1/items/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "name": "Volvo",
        "description": "Volvo from Germany",
    }


@pytest.mark.parametrize(
    "page, items_per_page, expected_json_response",
    [
        # Page is not greater than 0
        (
            0,
            10,
            {"error_message": "page: ensure this value is greater than 0"},
        ),
        # Items_per_page is not greater than 0
        (
            1,
            0,
            {"error_message": "items_per_page: ensure this value is greater than 0"},
        ),
        # Page is not an integer
        (
            "a",
            10,
            {"error_message": "page: value is not a valid integer"},
        ),
        # Items_per_page is not an integer
        (
            5,
            "a",
            {"error_message": "items_per_page: value is not a valid integer"},
        ),
    ],
)
async def test_fail_get_items_with_invalid_query_parameters(
    client: AsyncClient,
    list_items_creation: None,
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
    list_items_creation: None,
    page: int,
    items_per_page: int,
    expected_json_response_list_length: dict,
):
    response = await client.get(f"/categories/1/items?page={page}&items_per_page={items_per_page}")
    items_data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert items_data["total_number_of_items"] == 30
    assert items_data["items_per_page"] == items_per_page
    assert len(items_data["items"]) == expected_json_response_list_length


async def test_get_items_successfully_without_query_parameters(client: AsyncClient, list_items_creation: None):
    response = await client.get("/categories/1/items")
    items_data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert len(items_data["items"]) == 20
    assert items_data["items_per_page"] == 20


@pytest.mark.parametrize(
    "item_id, expected_status_code, expected_json_response",
    [
        # Item id is invalid
        (
            "a",
            status.HTTP_400_BAD_REQUEST,
            {"error_message": "item_id: value is not a valid integer"},
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
    item_creation: None,
    item_id: Union[int, str],
    expected_status_code: int,
    expected_json_response: dict,
):
    response = await client.get(f"/categories/1/items/{item_id}")
    assert response.status_code == expected_status_code
    assert response.json() == expected_json_response


async def test_get_single_item_successfully(client: AsyncClient, item_creation: None):
    response = await client.get("/categories/1/items/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"name": "Volvo", "description": "Volvo from Germany"}


async def test_fail_to_update_item_without_authentication(
    client: AsyncClient,
    access_token: str,
    item_creation: None,
):
    response = await client.put(
        "/categories/1/items/1",
        json={"description": "new description"},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"error_message": "User needs to authenticate"}


async def test_fail_to_update_item_without_ownership(
    client: AsyncClient,
    access_token: str,
    access_token_other_user: str,
    item_creation: None,
):
    # Other user tries to delete item
    response = await client.put(
        "/categories/1/items/1",
        headers=generate_authorization_header(access_token_other_user),
        json={"description": "new description"},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"error_message": "User does not have permission to perform this action"}


async def test_fail_to_update_item_with_non_existent_item(
    client: AsyncClient,
    access_token: str,
    item_creation: None,
):
    response = await client.put(
        "/categories/1/items/10",
        headers=generate_authorization_header(access_token),
        json={"description": "new description"},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"error_message": "Cannot find the specified item"}


async def test_fail_to_update_item_with_invalid_item_id(
    client: AsyncClient,
    access_token: str,
    item_creation: None,
):
    response = await client.put(
        "/categories/1/items/a",
        headers=generate_authorization_header(access_token),
        json={"description": "new description"},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"error_message": "item_id: value is not a valid integer"}


async def test_update_item_successfully(
    client: AsyncClient,
    access_token: str,
    item_creation: None,
):
    response = await client.put(
        "/categories/1/items/1",
        headers=generate_authorization_header(access_token),
        json={"description": "new description"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {}

    # Test if item is updated
    response = await client.get("/categories/1/items/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("description") == "new description"


async def test_fail_to_delete_item_without_authentication(
    client: AsyncClient,
    access_token: str,
    item_creation: None,
):
    response = await client.delete("/categories/1/items/1")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"error_message": "User needs to authenticate"}


async def test_fail_to_delete_item_without_ownership(
    client: AsyncClient,
    access_token: str,
    access_token_other_user: str,
    item_creation: None,
):
    # Other user tries to delete item
    response = await client.delete(
        "/categories/1",
        headers=generate_authorization_header(access_token_other_user),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"error_message": "User does not have permission to perform this action"}


async def test_fail_to_delete_item_with_non_existent_item(
    client: AsyncClient,
    access_token: str,
    item_creation: None,
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
    item_creation: None,
):
    response = await client.delete(
        "/categories/1/items/a",
        headers=generate_authorization_header(access_token),
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"error_message": "item_id: value is not a valid integer"}


async def test_delete_item_successfully(
    client: AsyncClient,
    access_token: str,
    item_creation: None,
):
    response = await client.delete(
        "/categories/1/items/1",
        headers=generate_authorization_header(access_token),
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {}

    # Test if item is deleted
    response = await client.get("/categories/1/items/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"error_message": "Cannot find the specified item"}
