from abc import ABC, abstractmethod
from typing import Any

import sqlalchemy as sa
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models import TypeModel


class BaseCrud(ABC):
    @abstractmethod
    async def create_item(self, data: dict[str, Any]):
        raise NotImplementedError

    @abstractmethod
    async def get_items(self):
        raise NotImplementedError

    @abstractmethod
    async def get_user(self, email):
        raise NotImplementedError


class SQLAlchemyCrud(BaseCrud):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.model: TypeModel

    async def create_item(self, data: dict[str, Any]):
        try:
            stmt = sa.insert(self.model).returning(self.model).values(**data)
            response = await self.session.scalar(stmt)
        except IntegrityError as error:
            if error.orig is not None and "uq_" in error.orig.args[0]:
                raise HTTPException(
                    status.HTTP_400_BAD_REQUEST,
                    f"{self.model.__name__} already exists",
                ) from error
            raise error
        return response

    async def get_items(self):
        stmt = sa.select(self.model)
        response = await self.session.scalars(stmt)
        return response.unique().all()

    async def get_user(self, email: str):
        stmt = sa.select(self.model).where(self.model.email == email)
        user = await self.session.scalar(stmt)
        if user is None:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND, f"{email} not found"
            )
        return user
