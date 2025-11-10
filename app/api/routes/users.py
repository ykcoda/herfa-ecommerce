from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.database.schemas.user import ReadUser, CreateUser, UpdateUser
from app.api.common.dependencies import USER_SERVICE_DEP, AUTHENTICATED_USER_DEP
from app.utils import logging_service, LogServiceType, LogType, redis_service
from uuid import UUID
from typing import Annotated

# create an endpoint router for users
users = APIRouter(prefix="/api/users", tags=["Users"])


@users.get("/", response_model=list[ReadUser])
async def get_all_users(
    service: USER_SERVICE_DEP,
    authorized_user: AUTHENTICATED_USER_DEP,
):

    return await service.get_all_user()


# register new user
@users.post("/register")
async def register_user(data: CreateUser, service: USER_SERVICE_DEP):
    return await service.create_user(data)


# update a user
@users.put("/update")
async def update_user(
    id: UUID,
    data: UpdateUser,
    service: USER_SERVICE_DEP,
    authorized_user: AUTHENTICATED_USER_DEP,
):
    return await service.update_user(id, data)


# delete a user
@users.delete("/delete")
async def delete_user(
    id: UUID,
    service: USER_SERVICE_DEP,
    authorized_user: AUTHENTICATED_USER_DEP,
):
    return await service.delete_user(id)


# login user and generate jwt token
@users.post("/token")
async def login_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: USER_SERVICE_DEP,
):
    # request for user access token
    token = await service.login_user(form_data.username, form_data.password)

    if token:
        # log
        logging_service.set_log(f"{form_data.username} has successfully login..", log_service_type=LogServiceType.ENDPOINT, log_type=LogType.INFO)  # type: ignore

        return {
            "access_token": token,
            "token_type": "jwt",
        }


# logout user
@users.post("/logout")
async def logout_user(authorized_user: AUTHENTICATED_USER_DEP):
    if authorized_user:
        # log
        logging_service.set_log(f"{authorized_user['user']['email']} has logout..", log_service_type=LogServiceType.ENDPOINT, log_type=LogType.INFO)  # type: ignore

        # save authorized users jti access token to redis
        await redis_service.save_to_redis(authorized_user["jti"])  # type: ignore
        return {"detail": "User has successfully logout."}
