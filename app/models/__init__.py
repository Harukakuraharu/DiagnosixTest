from typing import Type, TypeVar

from models.base import Base
from models.users_models import User, UserRole

MODEL = TypeVar("MODEL", bound=Base)

TypeModel = Type[MODEL]
