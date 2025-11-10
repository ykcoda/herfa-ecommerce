from fastapi import APIRouter
from app.database.schemas.user import UserCreate, UserRead, UserUpdate
from app.api.common.dependencies import USER_SERVICE_DEP
from uuid import UUID

# create an endpoint router for users
users = APIRouter(prefix="/api/users", tags=["Users"])


@users.get("/", response_model=list[UserRead])
async def get_all_users(service: USER_SERVICE_DEP):
    return await service.get_all_user()


# register new user
@users.post("/register")
async def register_user(data: UserCreate, service: USER_SERVICE_DEP):
    return await service.create_user(data)


# update a user
@users.put("/update")
async def update_user(id: UUID, data: UserUpdate, service: USER_SERVICE_DEP):
    return await service.update_user(id, data)


# delete a user
@users.delete("/delete")
async def delete_user(id: UUID, service: USER_SERVICE_DEP):
    return await service.delete_user(id)
