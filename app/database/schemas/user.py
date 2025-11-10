from sqlmodel import SQLModel
from pydantic import EmailStr
from datetime import datetime
from uuid import UUID

from app.database.model.user import UserRole


class BaseUser(SQLModel):
    first_name: str
    last_name: str
    email: EmailStr
    role: UserRole
    active: bool = False
    password: str
    phone_number: str


class CreateUser(BaseUser):
    pass


class ReadUser(SQLModel):
    id: UUID
    first_name: str
    last_name: str
    email: EmailStr
    role: UserRole
    active: bool
    deleted: bool
    updated_at: datetime
    created_at: datetime


class ReadProductUser(SQLModel):
    email: EmailStr
    role: UserRole

    model_config = {"from_attributes": True}


class UpdateUser(SQLModel):
    first_name: str | None = None
    last_name: str | None = None
    role: UserRole | None = None
    active: bool | None = None
    deleted: bool | None = None
    phone_number: str | None = None
