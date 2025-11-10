from sqlmodel import SQLModel
from uuid import UUID


class BaseCategory(SQLModel):
    name: str
    description: str


class ReadCategory(BaseCategory):
    id: UUID


class ReadProductCategory(SQLModel):
    name: str
    description: str

    model_config = {"from_attributes": True}


class CreateCategory(BaseCategory):
    pass


class UpdateCategory(SQLModel):
    name: str | None = None
    description: str | None = None
    deleted: bool | None = None
