import pytest
from fastapi import status
from httpx import AsyncClient

INVALID_EMAIL_CASES = [
    # Email has space
    (
        {
            "email": "minh @gmail.com",
            "password": "String123",
        },
        {"error_message": "email: value is not a valid email address"},
    ),
    # Email does not contain '@'
    (
        {
            "email": "minhgmail.com",
            "password": "String123",
        },
        {"error_message": "email: value is not a valid email address"},
    ),
    # Email does not contain .label
    (
        {
            "email": "minh@gmail",
            "password": "String123",
        },
        {"error_message": "email: value is not a valid email address"},
    ),
    # Email has more than 1 '@'
    (
        {
            "email": "min@h@gmail",
            "password": "String123",
        },
        {"error_message": "email: value is not a valid email address"},
    ),
]

INVALID_PASSWORD_CASES = [
    # Password does not contain digit
    (
        {
            "email": "minh@gmail.com",
            "password": "Stringtext",
        },
        {
            "error_message": "password: Password must have at least 6 characters, "
            "including at least one lowercase letter, "
            "one uppercase letter, one digit."
        },
    ),
    # Password does not contain lowercase letter
    (
        {
            "email": "minh@gmail.com",
            "password": "STRING123",
        },
        {
            "error_message": "password: Password must have at least 6 characters, "
            "including at least one lowercase letter, "
            "one uppercase letter, one digit."
        },
    ),
    # Password does not contain uppercase letter
    (
        {
            "email": "minh@gmail.com",
            "password": "string123",
        },
        {
            "error_message": "password: Password must have at least 6 characters, "
            "including at least one lowercase letter, "
            "one uppercase letter, one digit."
        },
    ),
    # Password length is less than 6 characters
    (
        {
            "email": "minh@gmail.com",
            "password": "Strin",
        },
        {"error_message": "password: ensure this value has at least 6 characters"},
    ),
    # Password length is longer than 50 characters
    (
        {
            "email": "minh@gmail.com",
            "password": "String123" + "x" * 50,
        },
        {"error_message": "password: ensure this value has at most 50 characters"},
    ),
    # Password length is 51 characters
    (
        {
            "email": "minh@gmail.com",
            "password": "String123" + "x" * 42,
        },
        {"error_message": "password: ensure this value has at most 50 characters"},
    ),
]


@pytest.mark.parametrize(
    "user_credentials, expected_json_response",
    INVALID_EMAIL_CASES,
)
async def test_fail_to_register_user_with_invalid_email(
    client: AsyncClient,
    user_credentials: dict,
    expected_json_response: dict,
):
    user_credentials_copy = dict(user_credentials)
    user_credentials_copy.update({"full_name": "tester"})
    response = await client.post("/users", json=user_credentials_copy)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == expected_json_response


@pytest.mark.parametrize(
    "user_credentials, expected_json_response",
    [
        # Full_name length exceeds 50 characters
        (
            {
                "email": "minh@gmail.com",
                "password": "String123",
                "full_name": "Hoang Minh" + "h" * 50,
            },
            {"error_message": "full_name: ensure this value has at most 50 characters"},
        ),
        # Full_name length is 51 characters
        (
            {
                "email": "minh@gmail.com",
                "password": "String123",
                "full_name": "H" * 51,
            },
            {"error_message": "full_name: ensure this value has at most 50 characters"},
        ),
        # Full_name length is less than 1 character
        (
            {
                "email": "minh@gmail.com",
                "password": "String123",
                "full_name": "",
            },
            {"error_message": "full_name: ensure this value has at least 1 characters"},
        ),
    ],
)
async def test_fail_to_register_user_with_invalid_full_name(
    client: AsyncClient,
    user_credentials: dict,
    expected_json_response: dict,
):
    response = await client.post("/users", json=user_credentials)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == expected_json_response


@pytest.mark.parametrize(
    "user_credentials, expected_json_response",
    INVALID_PASSWORD_CASES,
)
async def test_fail_to_register_user_with_invalid_password(
    client: AsyncClient,
    user_credentials: dict,
    expected_json_response: dict,
):
    user_credentials_copy = dict(user_credentials)
    user_credentials_copy.update({"full_name": "tester"})
    response = await client.post("/users", json=user_credentials_copy)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == expected_json_response


async def test_fail_to_register_user_with_existed_name(client: AsyncClient):
    await client.post(
        "/users",
        json={
            "email": "email0@example.com",
            "password": "String123",
            "full_name": "Hoang Minh",
        },
    )
    response = await client.post(
        "/users",
        json={
            "email": "email0@example.com",
            "password": "String123",
            "full_name": "Hoang Minh",
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"error_message": "This email is already registered"}


async def test_register_user_successfully(client: AsyncClient):
    response = await client.post(
        "/users",
        json={
            "email": "email0@example.com",
            "password": "String123",
            "full_name": "Hoang Minh",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {}

    # Test if user is registered on the server
    response = await client.post(
        "/users/auth",
        json={
            "email": "email0@example.com",
            "password": "String123",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()


@pytest.mark.parametrize(
    "user_credentials, expected_json_response",
    INVALID_EMAIL_CASES,
)
async def test_fail_to_login_with_invalid_email(
    client: AsyncClient,
    user_credentials: dict,
    expected_json_response: dict,
):
    response = await client.post("/users/auth", json=user_credentials)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == expected_json_response


@pytest.mark.parametrize(
    "user_credentials, expected_json_response",
    INVALID_PASSWORD_CASES,
)
async def test_fail_to_login_with_invalid_password(
    client: AsyncClient,
    user_credentials: dict,
    expected_json_response: dict,
):
    response = await client.post("/users/auth", json=user_credentials)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == expected_json_response


async def test_fail_to_login_with_unregistered_email(client: AsyncClient):
    response = await client.post(
        "/users/auth",
        json={
            "email": "email0@example.com",
            "password": "String123",
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"error_message": "Invalid email or password"}


async def test_fail_to_login_with_wrong_password(client: AsyncClient):
    # Register
    await client.post(
        "/users",
        json={
            "email": "email0@example.com",
            "password": "String123",
            "full_name": "Hoang Minh",
        },
    )
    # Login
    response = await client.post(
        "/users/auth",
        json={
            "email": "email0@example.com",
            "password": "String123___0",
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"error_message": "Invalid email or password"}


async def test_login_successfully(client: AsyncClient):
    # Register
    await client.post(
        "/users",
        json={
            "email": "email0@example.com",
            "password": "String123",
            "full_name": "Hoang Minh",
        },
    )
    # Login
    response = await client.post(
        "/users/auth",
        json={
            "email": "email0@example.com",
            "password": "String123",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
