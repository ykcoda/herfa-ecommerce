from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime


class Category(SQLModel, table=True):
    __tablename__ = "categories"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    description: str
    created_at: datetime = Field(default_factory=datetime.now)
