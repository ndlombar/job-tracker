import uuid
from datetime import date

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base


class Application(Base):
    __tablename__ = "applications"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    company: Mapped[str] = mapped_column(String(30))
    role: Mapped[str] = mapped_column(String(30))
    status: Mapped[str] = mapped_column(String(15))
    source: Mapped[str] = mapped_column(String(15))
    applied_date: Mapped[date]

    user: Mapped["User"] = relationship(back_populates="applications")
    contacts: Mapped[list["Contact"]] = relationship(back_populates="application", cascade="all, delete-orphan")
    interviews: Mapped[list["Interview"]] = relationship(back_populates="application", cascade="all, delete-orphan")
    status_events: Mapped[list["StatusEvent"]] = relationship(back_populates="application", cascade="all, delete-orphan")