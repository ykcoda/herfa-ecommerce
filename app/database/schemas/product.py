from sqlmodel import SQLModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.database.schemas.category import ReadCategory, ReadProductCategory
from app.database.schemas.user import ReadProductUser


class BaseProduct(SQLModel):
    name: str
    description: str
    price: float
    stock_quantity: int


class ReadProduct(BaseProduct):
    name: str
    description: str
    price: float
    stock_quantity: int
    active: bool
    created_at: datetime
    updated_at: datetime
    category_id: UUID
    user_id: UUID

    category: Optional[ReadProductCategory] = None
    user: Optional[ReadProductUser] = None

    model_config = {"from_attributes": True}


class CreateProduct(BaseProduct):
    category_id: UUID = Field(description="The category this product belongs to")


class UpdateProduct(SQLModel):
    category_id: UUID | None = None
    name: str | None = None
    description: str | None = None
    price: float | None = None
    stock_quantity: int | None = None
    active: bool | None = None
