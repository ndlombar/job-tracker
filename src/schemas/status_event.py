import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class StatusEventBase(BaseModel):
    old_status: str
    new_status: str
    changed_at: datetime


class StatusEventCreate(StatusEventBase):
    application_id: uuid.UUID


class StatusEventUpdate(BaseModel):
    old_status: str | None = None
    new_status: str | None = None
    changed_at: datetime | None = None


class StatusEventRead(StatusEventBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    application_id: uuid.UUID
