from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.database.model.user import User
    from app.database.model.category import Category


class Product(SQLModel, table=True):
    __tablename__ = "products"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    description: str
    price: float
    stock_quantity: int
    active: bool = Field(default=True)
    deleted: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # Foreign keys
    category_id: UUID = Field(foreign_key="categories.id")
    user_id: UUID = Field(foreign_key="users.id")

    # Relationship
    category: "Category" = Relationship(
        back_populates="products", sa_relationship_kwargs={"lazy": "selectin"}
    )

    user: "User" = Relationship(
        back_populates="products", sa_relationship_kwargs={"lazy": "selectin"}
    )
