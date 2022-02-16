from fastapi import status
import pytest


async def test_create_category_unauthenticated(client):
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
    "category_data, expected_status_code, expected_json_response",
    [
        # name length is less than 1
        (
            {"name": "", "description": "Car has 4 wheels"},
            status.HTTP_400_BAD_REQUEST,
            {"error_message": "ensure this value has at least 1 characters"},
        ),
        # name length is greater than 50
        (
            {"name": "Carrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr", "description": "Car has 4 wheels"},
            status.HTTP_400_BAD_REQUEST,
            {"error_message": "ensure this value has at most 50 characters"},
        ),
    ],
)
async def test_create_category_invalid_name_length(
    client,
    access_token,
    category_data,
    expected_status_code,
    expected_json_response,
):
    response = await client.post(
        "/categories",
        headers={"Authorization": f"Bearer {access_token}"},
        json=category_data,
    )
    assert response.status_code == expected_status_code
    assert response.json() == expected_json_response


@pytest.mark.parametrize(
    "category_data, expected_status_code, expected_json_response",
    [
        # description length is less than 1
        (
            {"name": "Car", "description": ""},
            status.HTTP_400_BAD_REQUEST,
            {"error_message": "ensure this value has at least 1 characters"},
        ),
        # description length is greater than 50
        (
            {"name": "Car", "description": "Car has 4 wheels" + "s" * 5000},
            status.HTTP_400_BAD_REQUEST,
            {"error_message": "ensure this value has at most 5000 characters"},
        ),
    ],
)
async def test_create_category_invalid_description_length(
    client,
    access_token,
    category_data,
    expected_status_code,
    expected_json_response,
):
    response = await client.post(
        "/categories",
        headers={"Authorization": f"Bearer {access_token}"},
        json=category_data,
    )
    assert response.status_code == expected_status_code
    assert response.json() == expected_json_response


async def test_create_category_name_exist(client, access_token):
    category_data = {"name": "Car", "description": "Car has 4 wheels"}
    await client.post(
        "/categories",
        headers={"Authorization": f"Bearer {access_token}"},
        json=category_data,
    )
    response = await client.post(
        "/categories",
        headers={"Authorization": f"Bearer {access_token}"},
        json=category_data,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"error_message": "Category already exists"}


async def test_create_category_successfully(client, access_token):
    response = await client.post(
        "/categories",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"name": "Car", "description": "Car has 4 wheels"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {}


async def test_get_categories(client, access_token):
    # create categories
    await client.post(
        "/categories",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"name": "Car", "description": "Car has 4 wheels"},
    )
    await client.post(
        "/categories",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"name": "Bike", "description": "Bike has 2 wheels"},
    )
    # get categories
    response = await client.get("/categories")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{"id": 1, "name": "Car"}, {"id": 2, "name": "Bike"}]


@pytest.mark.parametrize(
    "category_id, expected_status_code, expected_json_response",
    [
        # category id is invalid
        (
            "a",
            status.HTTP_400_BAD_REQUEST,
            {"error_message": "value is not a valid integer"},
        ),
        # category id does not exist
        (
            10,
            status.HTTP_404_NOT_FOUND,
            {"error_message": "Cannot find the specified category"},
        ),
    ],
)
async def test_get_single_category_unsuccessfully(
    client, create_category, category_id, expected_status_code, expected_json_response
):
    response = await client.get(f"/categories/{category_id}")
    assert response.status_code == expected_status_code
    assert response.json() == expected_json_response


async def test_get_single_category_successfully(client, access_token, create_category):
    response = await client.get("/categories/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"name": "Car", "description": "Car has 4 wheels"}


async def test_delete_category_unauthenticated(client, access_token, create_category):
    response = await client.delete("/categories/1")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"error_message": "User needs to authenticate"}


async def test_delete_category_not_owner(client, access_token, create_category, access_token_other_user):
    # other user tries to delete category
    response = await client.delete(
        "/categories/1",
        headers={"Authorization": f"Bearer {access_token_other_user}"},
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"error_message": "User does not have permission to perform this action"}


async def test_delete_category_not_found(client, access_token, create_category):
    response = await client.delete(
        "/categories/10",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"error_message": "Cannot find the specified category"}


async def test_delete_category_invalid_category_id(client, access_token, create_category):
    response = await client.delete(
        "/categories/a",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"error_message": "value is not a valid integer"}


async def test_delete_category_successfully(client, access_token, create_category):
    response = await client.delete(
        "/categories/1",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {}
