from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr
from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.database.model.product import Product


class UserRole(str, Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    first_name: str
    last_name: str
    email: EmailStr = Field(unique=True)
    password_hash: str
    phone_number: str
    role: UserRole = Field(default=UserRole.ADMIN)
    active: bool = Field(default=True)
    deleted: bool = Field(default=False, nullable=True)
    updated_at: datetime = Field(default_factory=datetime.now)
    created_at: datetime = Field(default_factory=datetime.now)

    # Relationship
    products: list["Product"] | None = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )
