from fastapi.routing import APIRouter
from services.users_services import UserService

from core import dependency
from schemas import users_schemas


user_routers = APIRouter(
    prefix="/user",
    tags=["User"],
)


@user_routers.post("/registration/", response_model=users_schemas.UserResponse)
async def create_user(
    session: dependency.AsyncSessionDependency, data: users_schemas.UserCreate
):
    """Registration of all user"""
    return await UserService(session).create_user(data)


@user_routers.post("/auth/", response_model=users_schemas.Token)
async def login(
    session: dependency.AsyncSessionDependency, data: users_schemas.UserLogin
):
    """Auth user"""
    return await UserService(session).login(data)


@user_routers.get("/me/", response_model=users_schemas.UserResponse)
async def get_users_me(
    current_user: dependency.GetCurrentUserDependency,
):
    """Get info about current user"""
    return current_user
