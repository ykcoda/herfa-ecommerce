from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import TypeVar, Generic, Type, Sequence, Any
from uuid import UUID


T = TypeVar("T", bound="SQLModel")  # declare a generic type for Models


class BaseService(Generic[T]):
    """BaseService that executes Common CRUD Operations."""

    def __init__(self, model: Type[T], session: AsyncSession):
        self.model = model
        self.session = session

    # resturn a single entity by passing its id
    async def _get(self, id: UUID):
        """Get a single entity by passing its id"""
        return await self.session.get(self.model, id)

    # Get all entires for an entity
    async def _get_all(self) -> Sequence[T] | None:
        """Return a sequence of an entity"""
        statement = select(self.model)
        result = await self.session.exec(statement=statement)
        return result.all()

    # create an entity
    async def _create(self, entity: Any) -> Type[T]:
        """Create a new entity"""
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    # update an entity
    async def _update(self, entity: Any) -> Type[T]:
        """Updates an entity"""
        await self._create(entity)
        return entity

    # delete an entity
    async def _delete(self, entity: Any) -> bool:
        """Delete an entity"""
        await self.session.delete(entity)
        await self.session.commit()
        return True
