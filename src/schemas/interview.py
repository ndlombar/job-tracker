import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class InterviewBase(BaseModel):
    stage: str
    scheduled_at: datetime
    notes: str


class InterviewCreate(InterviewBase):
    application_id: uuid.UUID


class InterviewUpdate(BaseModel):
    stage: str | None = None
    scheduled_at: datetime | None = None
    notes: str | None = None


class InterviewRead(InterviewBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    application_id: uuid.UUID
