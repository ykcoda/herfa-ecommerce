from uuid import UUID
from fastapi import APIRouter
from app.api.common.dependencies import AUTHENTICATED_USER_DEP, CATEGORY_SERVICE_DEP
from app.database.schemas.category import CreateCategory, UpdateCategory

categories = APIRouter(
    prefix="/api/categories",
    tags=["Categories"],
    include_in_schema=True,
)


# get all categories
@categories.get("/")
async def all_categories(
    service: CATEGORY_SERVICE_DEP,
    authenticated_user: AUTHENTICATED_USER_DEP,
):
    return await service.get_all_categories()


# create new category
@categories.post("/create")
async def create_category(
    data: CreateCategory,
    service: CATEGORY_SERVICE_DEP,
    authenticated_user: AUTHENTICATED_USER_DEP,
):
    return await service.create_category(data)


# update category
@categories.put("/update")
async def update_category(
    id: UUID,
    data: UpdateCategory,
    service: CATEGORY_SERVICE_DEP,
    authenticated_user: AUTHENTICATED_USER_DEP,
):
    return await service.update_category(id, data)


# delete category
@categories.delete("/delete")
async def delete_category(
    id: UUID,
    service: CATEGORY_SERVICE_DEP,
    authenticated_user: AUTHENTICATED_USER_DEP,
):
    return await service.delete_category(id)
