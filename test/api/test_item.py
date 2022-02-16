from fastapi import status
import pytest


async def test_create_item_unauthenticated(client, create_item):
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
    "item_data, expected_status_code, expected_json_response",
    [
        # name length is less than 1
        (
            {"name": "", "description": "Volvo from Germany"},
            status.HTTP_400_BAD_REQUEST,
            {"error_message": "ensure this value has at least 1 characters"},
        ),
        # name length is greater than 50
        (
            {"name": "Volvo" + "o" * 50, "description": "Volvo from Germany"},
            status.HTTP_400_BAD_REQUEST,
            {"error_message": "ensure this value has at most 50 characters"},
        ),
    ],
)
async def test_create_item_invalid_name_length(
    client,
    access_token,
    create_category,
    item_data,
    expected_status_code,
    expected_json_response,
):
    response = await client.post(
        "/categories/1/items",
        headers={"Authorization": f"Bearer {access_token}"},
        json=item_data,
    )
    assert response.status_code == expected_status_code
    assert response.json() == expected_json_response


@pytest.mark.parametrize(
    "item_data, expected_status_code, expected_json_response",
    [
        # description length is less than 1
        (
            {"name": "Volvo", "description": ""},
            status.HTTP_400_BAD_REQUEST,
            {"error_message": "ensure this value has at least 1 characters"},
        ),
        # description length is greater than 50
        (
            {"name": "Volvo", "description": "Volvo from Germany" + "s" * 5000},
            status.HTTP_400_BAD_REQUEST,
            {"error_message": "ensure this value has at most 5000 characters"},
        ),
    ],
)
async def test_create_item_invalid_description_length(
    client,
    access_token,
    create_category,
    item_data,
    expected_status_code,
    expected_json_response,
):
    response = await client.post(
        "/categories/1/items",
        headers={"Authorization": f"Bearer {access_token}"},
        json=item_data,
    )
    assert response.status_code == expected_status_code
    assert response.json() == expected_json_response


async def test_create_item_name_exist(client, access_token, create_category):
    item_data = {"name": "Volvo", "description": "Volvo from Germany"}
    await client.post(
        "/categories/1/items",
        headers={"Authorization": f"Bearer {access_token}"},
        json=item_data,
    )
    response = await client.post(
        "/categories/1/items",
        headers={"Authorization": f"Bearer {access_token}"},
        json=item_data,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"error_message": "Item already exists"}


async def test_create_item_successfully(client, access_token, create_category):
    response = await client.post(
        "/categories/1/items",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"name": "Volvo", "description": "Volvo from Germany"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {}


@pytest.mark.parametrize(
    "page, items_per_page, expected_json_response",
    [
        (
            0,
            10,
            {"error_message": "ensure this value is greater than 0"},
        ),
        (
            1,
            0,
            {"error_message": "ensure this value is greater than 0"},
        ),
        (
            "a",
            10,
            {"error_message": "value is not a valid integer"},
        ),
        (
            5,
            "a",
            {"error_message": "value is not a valid integer"},
        ),
    ],
)
async def test_get_items_unsuccessfully(
    client, access_token, create_many_items, page, items_per_page, expected_json_response
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
    client, access_token, create_many_items, page, items_per_page, expected_json_response_list_length
):
    response = await client.get(f"/categories/1/items?page={page}&items_per_page={items_per_page}")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == expected_json_response_list_length


async def test_get_items_successfully_default_value(client, access_token, create_many_items):
    response = await client.get("/categories/1/items")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 20


async def test_get_single_item_successfully(client, access_token, create_item):
    response = await client.get("/categories/1/items/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"name": "Volvo", "description": "Volvo from Germany"}


@pytest.mark.parametrize(
    "item_id, expected_status_code, expected_json_response",
    [
        # item id is invalid
        (
            "a",
            status.HTTP_400_BAD_REQUEST,
            {"error_message": "value is not a valid integer"},
        ),
        # item id does not exist
        (
            10,
            status.HTTP_404_NOT_FOUND,
            {"error_message": "Cannot find the specified item"},
        ),
    ],
)
async def test_get_single_item_unsuccessfully(
    client, access_token, create_item, item_id, expected_status_code, expected_json_response
):
    response = await client.get(f"/categories/1/items/{item_id}")
    assert response.status_code == expected_status_code
    assert response.json() == expected_json_response


async def test_delete_item_unauthenticated(client, access_token, create_item):
    response = await client.delete("/categories/1/items/1")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"error_message": "User needs to authenticate"}


async def test_delete_item_not_owner(client, access_token, access_token_other_user, create_item):
    # other user tries to delete item
    response = await client.delete(
        "/categories/1",
        headers={"Authorization": f"Bearer {access_token_other_user}"},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"error_message": "User does not have permission to perform this action"}


async def test_delete_item_not_found(client, access_token, create_item):
    response = await client.delete(
        "/categories/1/items/10",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"error_message": "Cannot find the specified item"}


async def test_delete_item_invalid_item_id(client, access_token, create_item):
    response = await client.delete(
        "/categories/1/items/a",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"error_message": "value is not a valid integer"}


async def test_delete_item_successfully(client, access_token, create_item):
    response = await client.delete(
        "/categories/1/items/1",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {}
