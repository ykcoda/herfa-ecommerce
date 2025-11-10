from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.database.model.product import Product


class Category(SQLModel, table=True):
    __tablename__ = "categories"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    description: str
    created_at: datetime = Field(default_factory=datetime.now)

    # Relationship
    products: list["Product"] = Relationship(
        back_populates="category", sa_relationship_kwargs={"lazy": "selectin"}
    )
