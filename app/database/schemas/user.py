from sqlmodel import SQLModel, Field
from pydantic import EmailStr
from datetime import datetime
from uuid import UUID

from app.database.model.user import UserRole


class UserBase(SQLModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    phone_number: str


class UserRead(UserBase):
    id: UUID
    role: UserRole
    active: bool
    updated_at: datetime
    created_at: datetime


class UserCreate(UserBase):
    pass


class UserUpdate(SQLModel):
    first_name: str | None = None
    last_name: str | None = None
    role: UserRole
    active: bool | None = None
    phone_number: str | None = None
