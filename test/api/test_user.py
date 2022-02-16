from fastapi import status
import pytest


test_case_invalid_email = [
    # email has space
    (
        {
            "email": "minh @gmail.com",
            "password": "String123",
            "full_name": "Hoang Minh",
        },
        status.HTTP_400_BAD_REQUEST,
        {"error_message": "value is not a valid email address"},
    ),
    # email does not contain '@'
    (
        {
            "email": "minhgmail.com",
            "password": "String123",
            "full_name": "Hoang Minh",
        },
        status.HTTP_400_BAD_REQUEST,
        {"error_message": "value is not a valid email address"},
    ),
    # email does not contain .label
    (
        {
            "email": "minh@gmail",
            "password": "String123",
            "full_name": "Hoang Minh",
        },
        status.HTTP_400_BAD_REQUEST,
        {"error_message": "value is not a valid email address"},
    ),
    # email has more than 1 '@'
    (
        {
            "email": "min@h@gmail",
            "password": "String123",
            "full_name": "Hoang Minh",
        },
        status.HTTP_400_BAD_REQUEST,
        {"error_message": "value is not a valid email address"},
    ),
]

test_case_invalid_password = [
    (
        # password does not contain digit
        {
            "email": "minh@gmail.com",
            "password": "Stringtext",
            "full_name": "Hoang Minh",
        },
        status.HTTP_400_BAD_REQUEST,
        {
            "error_message": "Password must have at least 6 characters, "
            "including at least one lowercase letter, "
            "one uppercase letter, one digit."
        },
    ),
    (
        # password does not contain lowercase letter
        {
            "email": "minh@gmail.com",
            "password": "STRING123",
            "full_name": "Hoang Minh",
        },
        status.HTTP_400_BAD_REQUEST,
        {
            "error_message": "Password must have at least 6 characters, "
            "including at least one lowercase letter, "
            "one uppercase letter, one digit."
        },
    ),
    (
        # password does not contain uppercase letter
        {
            "email": "minh@gmail.com",
            "password": "string123",
            "full_name": "Hoang Minh",
        },
        status.HTTP_400_BAD_REQUEST,
        {
            "error_message": "Password must have at least 6 characters, "
            "including at least one lowercase letter, "
            "one uppercase letter, one digit."
        },
    ),
    (
        # password length is less than 6 characters
        {
            "email": "minh@gmail.com",
            "password": "Strin",
            "full_name": "Hoang Minh",
        },
        status.HTTP_400_BAD_REQUEST,
        {"error_message": "ensure this value has at least 6 characters"},
    ),
    (
        # password length is longer than 50 characters
        {
            "email": "minh@gmail.com",
            "password": "String123xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            "full_name": "Hoang Minh",
        },
        status.HTTP_400_BAD_REQUEST,
        {"error_message": "ensure this value has at most 50 characters"},
    ),
]


@pytest.mark.parametrize(
    "user_authentication_info, expected_status_code, expected_json_response", test_case_invalid_email
)
async def test_user_invalid_email(client, user_authentication_info, expected_status_code, expected_json_response):
    response = await client.post("/users", json=user_authentication_info)
    assert response.status_code == expected_status_code
    assert response.json() == expected_json_response


@pytest.mark.parametrize(
    "user_authentication_info, expected_status_code, expected_json_response",
    [
        # full_name length exceeds 50 characters
        (
            {
                "email": "minh@gmail.com",
                "password": "String123",
                "full_name": "Hoang Minhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh",
            },
            status.HTTP_400_BAD_REQUEST,
            {"error_message": "ensure this value has at most 50 characters"},
        ),
        # full_name length is less than 1 character
        (
            {
                "email": "minh@gmail.com",
                "password": "String123",
                "full_name": "",
            },
            status.HTTP_400_BAD_REQUEST,
            {"error_message": "ensure this value has at least 1 characters"},
        ),
    ],
)
async def test_user_register_invalid_full_name_length(
    client,
    user_authentication_info,
    expected_status_code,
    expected_json_response,
):
    response = await client.post("/users", json=user_authentication_info)
    assert response.status_code == expected_status_code
    assert response.json() == expected_json_response


@pytest.mark.parametrize(
    "user_authentication_info, expected_status_code, expected_json_response", test_case_invalid_password
)
async def test_user_register_invalid_password(
    client,
    user_authentication_info,
    expected_status_code,
    expected_json_response,
):
    response = await client.post("/users", json=user_authentication_info)
    assert response.status_code == expected_status_code
    assert response.json() == expected_json_response


async def test_user_register_email_exists(client):
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


async def test_user_register_successfully(client):
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


@pytest.mark.parametrize(
    "user_authentication_info, expected_status_code, expected_json_response", test_case_invalid_email
)
async def test_user_login_invalid_email(client, user_authentication_info, expected_status_code, expected_json_response):
    response = await client.post("/users/auth", json=user_authentication_info)
    assert response.status_code == expected_status_code
    assert response.json() == expected_json_response


@pytest.mark.parametrize(
    "user_authentication_info, expected_status_code, expected_json_response", test_case_invalid_password
)
async def test_user_login_invalid_password(
    client,
    user_authentication_info,
    expected_status_code,
    expected_json_response,
):
    response = await client.post("/users/auth", json=user_authentication_info)
    assert response.status_code == expected_status_code
    assert response.json() == expected_json_response


async def test_user_login_unregistered_email(client):
    response = await client.post(
        "/users/auth",
        json={
            "email": "email0@example.com",
            "password": "String123",
            "full_name": "Hoang Minh",
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"error_message": "Invalid email or password"}


async def test_user_login_successfully(client):
    # register
    await client.post(
        "/users",
        json={
            "email": "email0@example.com",
            "password": "String123",
            "full_name": "Hoang Minh",
        },
    )
    # login
    response = await client.post(
        "/users/auth",
        json={
            "email": "email0@example.com",
            "password": "String123",
            "full_name": "Hoang Minh",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
