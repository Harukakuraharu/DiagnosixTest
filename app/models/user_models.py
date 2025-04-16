import enum

from models.base import Base
from sqlalchemy import Integer, String, false
from sqlalchemy.orm import Mapped, mapped_column


class UserRole(enum.Enum):
    PATIENT = "patient"
    DOCTOR = "doctor"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(72))
    name: Mapped[str | None] = mapped_column(String(100))
    active: Mapped[bool] = mapped_column(server_default=false())
    role: Mapped[UserRole] = mapped_column(default=UserRole.PATIENT)
