import uuid
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base

if TYPE_CHECKING:
    from src.models.application import Application


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(40), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255))

    applications: Mapped[list["Application"]] = relationship(back_populates="user", cascade="all, delete-orphan")