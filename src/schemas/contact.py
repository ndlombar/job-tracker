import uuid
from datetime import date

from pydantic import BaseModel, ConfigDict

class ContactBase(BaseModel):
    name: str
    role: str
    email: str

class ContactCreate(ContactBase):
    application_id: uuid.UUID

class ContactUpdate(BaseModel):
    name: str | None = None
    role: str | None = None
    email: str | None = None

class ContactRead(ContactBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    application_id: uuid.UUID