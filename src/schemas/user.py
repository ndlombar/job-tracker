import uuid

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    hashed_password: str


class UserUpdate(BaseModel):
    email: str | None = None
    hashed_password: str | None = None


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
