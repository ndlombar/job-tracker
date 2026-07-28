import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base

if TYPE_CHECKING:
    from src.models.application import Application


class Interview(Base):
    __tablename__ = "interviews"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    application_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("applications.id"))
    stage: Mapped[str] = mapped_column(String(15))
    scheduled_at: Mapped[datetime]
    notes: Mapped[str] = mapped_column(String(255))

    application: Mapped["Application"] = relationship(back_populates="interviews")