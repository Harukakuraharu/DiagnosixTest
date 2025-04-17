import jwt
import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import models
from core import security
from core.config import config
from tests.tests_factory import users_facrory as fc


pytestmark = pytest.mark.anyio


TEST_PASSWORD = "qwerty123"
TEST_EMAIL = "user@test.com"


def test_hash_password():
    """Test hashing and checking password"""
    hashed_password = security.hash_password(TEST_PASSWORD)
    assert security.check_password(TEST_PASSWORD, hashed_password)
    assert not security.check_password("qwerty", hashed_password)


def test_create_access_token():
    """Create access token"""
    data = {"sub": TEST_EMAIL, "role": models.UserRole.PATIENT.value}
    access_token = security.create_access_token(data)
    assert isinstance(access_token, str)


def test_decode_token():
    """Decode token"""
    token_data = {"sub": TEST_EMAIL, "role": models.UserRole.PATIENT.value}
    token = security.create_access_token(token_data)
    decoded = jwt.decode(
        token, config.SECRET_KEY, algorithms=[config.ALGORITHM]
    )
    assert decoded["sub"] == TEST_EMAIL
    assert decoded["role"] == "patient"
    assert "exp" in decoded


async def test_authenticate_user_success(async_session: AsyncSession, factory):
    """Successful auth"""
    user = await factory(
        fc.UserFactory, password=TEST_PASSWORD, email=TEST_EMAIL
    )
    auth_user = await security.auth(async_session, user.email, TEST_PASSWORD)
    assert auth_user.email == user.email


async def test_authenticate_user_wrong_password(
    async_session: AsyncSession, factory
):
    """Auth with incorrect password"""
    incorrect_password = "hehehe"
    user = await factory(
        fc.UserFactory, password=TEST_PASSWORD, email=TEST_EMAIL
    )
    with pytest.raises(HTTPException) as exc:
        await security.auth(async_session, user.email, incorrect_password)
    assert exc.value.detail == "Incorrect password or username"


async def test_authenticate_user_not_exist(async_session: AsyncSession):
    """Auth not exists user"""
    with pytest.raises(HTTPException) as exc:
        await security.auth(async_session, "example@test.com", "password123")
    assert exc.value.detail == "User is not exists"
