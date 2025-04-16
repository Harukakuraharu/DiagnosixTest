from typing import Annotated, AsyncIterator

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from models import User, UserRole
from core.config import config
from crud.users_crud import UserCrud


ENGINE = create_async_engine(config.async_dsn)


async def get_session() -> AsyncIterator[AsyncSession]:
    """Get session for execution of the request"""
    async with AsyncSession(ENGINE) as session:
        yield session


AsyncSessionDependency = Annotated[
    AsyncSession, Depends(get_session, use_cache=True)
]


async def get_current_user(
    token: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())],
    session: AsyncSessionDependency,
) -> User:
    """Get current user who send request"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token.credentials, config.SECRET_KEY, algorithms=[config.ALGORITHM]
        )
        email: str = payload.get("sub", "")
        if email is None:
            raise credentials_exception
    except InvalidTokenError as err:
        raise credentials_exception from err
    user = await UserCrud(session).get_user(email)
    if user is None:
        raise credentials_exception
    return user


GetCurrentUserDependency = Annotated[User, Depends(get_current_user)]


# class RoleChecker:
#     """Depends for check user permissions"""

#     def __init__(self, allowed_roles: list[UserRole]):
#         self.allowed_roles = allowed_roles

#     def __call__(self, user: GetCurrentUserDependency) -> User:
#         if (
#             user.organization is None
#             or user.organization.role.name not in self.allowed_roles
#         ):
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 detail="You have not a permission to perform this action",
#             )
#         return user


# ManagerPermissionDependency = Annotated[
#     models.User,
#     Depends(
#         RoleChecker(
#             [models.UserRole.MANAGER.name, models.UserRole.SUPER_MANAGER.name]
#         )
#     ),
# ]

# EmployeerPermissionDependency = Annotated[
#     models.User,
#     Depends(RoleChecker([models.UserRole.EMPLOYEE])),
# ]