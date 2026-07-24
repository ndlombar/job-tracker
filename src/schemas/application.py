import uuid
from datetime import date

from pydantic import BaseModel, ConfigDict


class ApplicationBase(BaseModel):
    company: str
    role: str
    status: str
    source: str
    applied_date: date


class ApplicationCreate(ApplicationBase):
    user_id: uuid.UUID


class ApplicationUpdate(BaseModel):
    company: str | None = None
    role: str | None = None
    status: str | None = None
    source: str | None = None
    applied_date: date | None = None


class ApplicationRead(ApplicationBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
