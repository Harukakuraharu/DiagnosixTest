import pytest
from fastapi import status
from httpx import AsyncClient

import models
from tests.tests_factory import users_facrory as fc


pytestmark = pytest.mark.anyio


@pytest.mark.parametrize(
    "password, status_code",
    [
        ("qwerty123", status.HTTP_200_OK),
        ("qwerty", status.HTTP_422_UNPROCESSABLE_ENTITY),
        ("q123", status.HTTP_422_UNPROCESSABLE_ENTITY),
    ],
)
async def test_create_user(
    client: AsyncClient, password: str, status_code: status
):
    """Test create user with different password"""
    data = {
        "name": "Hello World",
        "email": "qwerty@mail.ru",
        "password": password,
        "role": models.UserRole.PATIENT.value,
    }
    response = await client.post("/user/registration/", json=data)
    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        data.pop("password")
        response.json().pop("id")
        assert all(
            response.json()[key] == data[key]
            for key in data  # pylint: disable=C0206
        )
        assert "password" not in response.json()


async def test_auth_user(client: AsyncClient, factory):
    """Auth user"""
    password = "string123"
    user = await factory(fc.UserFactory, password=password)
    data = {
        "email": user.email,
        "password": password,
    }
    response = await client.post("/user/auth/", json=data)
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()


async def test_auth_user_with_invalid_password(client: AsyncClient, factory):
    """Auth with incorrect password"""
    password = "string123"
    user = await factory(fc.UserFactory, password=password)
    data = {
        "email": user.email,
        "password": "string12345",
    }
    response = await client.post("/user/auth/", json=data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_get_user(user_client: AsyncClient):
    """Get info about youself"""
    response = await user_client.get("user/me/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Test_user"


async def test_get_user_not_auth(client: AsyncClient):
    response = await client.get("user/me/")
    assert response.status_code == status.HTTP_403_FORBIDDEN


async def test_get_user_with_invalid_token(client: AsyncClient, factory):
    """"""
    password = "string123"
    user = await factory(fc.UserFactory, password=password)
    data = {
        "email": user.email,
        "password": password,
    }
    response = await client.post("/user/auth/", json=data)
    assert response.status_code == status.HTTP_200_OK
    invalid_token = "sfrgtyu76543567uiuytredwasfgh"
    response = await client.get(
        "user/me/", headers={"WWW-Authenticate": f"Bearer {invalid_token}"}
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
