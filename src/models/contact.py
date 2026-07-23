import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base


class Contact(Base):
    __tablename__ = "contacts"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    application_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("applications.id"))
    name: Mapped[str] = mapped_column(String(40))
    role: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(40), unique=True)

    application: Mapped["Application"] = relationship(back_populates="contacts")
