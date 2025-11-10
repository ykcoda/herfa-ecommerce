from uuid import UUID
from fastapi import HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from app.database.model.category import Category
from app.api.service.base_service import BaseService
from app.database.schemas.category import CreateCategory, UpdateCategory
from app.utils import logging_service, LogType, LogServiceType


class CategoryService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(Category, session)
        self.session = session

    # get all categories
    async def get_all_categories(self):
        return await self._get_all()

    # create product category
    async def create_category(self, data: CreateCategory):
        # pass category data to Category Object
        new_data = Category(**data.model_dump())
        # log
        logging_service.set_log(
            f"{data.name} has been created.",
            log_type=LogType.INFO,
            log_service_type=LogServiceType.DATABASE,
        )
        # return created categoty
        return await self._create(new_data)

    # update category
    async def update_category(self, id: UUID, data: UpdateCategory):
        category = await self._get(id)
        if not category:
            # log
            logging_service.set_log(
                message=f"Category with id '{id}' doesn't exist",
                log_type=LogType.ERROR,
                log_service_type=LogServiceType.DATABASE,
            )
            # raise and exception if category is not found
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"category with id '{id}' doesn't exist",
            )
        # update the category with updated data
        return await self._update(
            category.sqlmodel_update(data.model_dump(exclude_none=True))
        )

    # delete category
    async def delete_category(self, id: UUID):
        category = await self._get(id)
        if not category:
            # log
            logging_service.set_log(
                message=f"Category with id '{id}' doesn't exist",
                log_type=LogType.ERROR,
                log_service_type=LogServiceType.DATABASE,
            )
            # raise and exception if category is not found
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category with id '{id}' doesn't exist",
            )
        # updated deleted attribute to True
        category.deleted = True

        # delete category
        await self._delete(category)

        # log
        logging_service.set_log(
            message=f"Category with id '{id}' has been deleted.",
            log_type=LogType.INFO,
            log_service_type=LogServiceType.DATABASE,
        )
        return {"detail": "Category deleted!"}
