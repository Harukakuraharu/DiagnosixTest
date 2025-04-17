from datetime import timedelta

from sqlalchemy.ext.asyncio import AsyncSession

import models
from core import security
from core.config import config
from crud.users_crud import UserCrud
from schemas import users_schemas


class UserService:
    """Execution of the request for user endpoint"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.crud = UserCrud(self.session)

    async def create_user(self, data: users_schemas.UserCreate) -> models.User:
        """Execution of the request for create user"""
        data.password = security.hash_password(data.password)

        user = await self.crud.create_item(data.model_dump())
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def login(
        self, data: users_schemas.UserLogin
    ) -> users_schemas.Token:
        """Execution of the request for login user"""
        user = await security.auth(self.session, data.email, data.password)
        access_token_expires = timedelta(
            minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        access_token = security.create_access_token(
            data={"sub": user.email, "role": user.role.value},
            expires_delta=access_token_expires,
        )
        return users_schemas.Token(access_token=access_token)
