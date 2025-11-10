from fastapi import HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.database.model.user import User
from app.api.service.base_service import BaseService
from app.database.schemas.user import UserCreate, UserUpdate
from datetime import datetime
from uuid import UUID
from app.utils import (
    logging_service,
    LogType,
    LogServiceType,
    generate_jwt_token,
    decode_encoded_jwt_token,
)

from pwdlib import PasswordHash


password_hash = PasswordHash.recommended()


class UserService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)
        self.session = session

    # get user by email
    async def get_user_by_email(self, email):
        statement = select(User).where(User.email == email)
        result = await self.session.exec(statement)
        return result.first()

    # get all users
    async def get_all_user(self):
        return await self._get_all()

    # create a user
    async def create_user(self, user: UserCreate):
        # check if email exists in uses table
        if not await self.get_user_by_email(user.email):
            # only create user if the email is not present in users table
            new_user = User(
                **user.model_dump(), password_hash=password_hash.hash(user.password)
            )
            # log
            logging_service.set_log(
                f"Registered a new user with email {user.email}",
                log_type=LogType.INFO,
                log_service_type=LogServiceType.DATABASE,
            )
            return await self._create(new_user)
        else:
            # log
            logging_service.set_log(
                f"User with this email({user.email}) already exists",
                log_type=LogType.ERROR,
                log_service_type=LogServiceType.DATABASE,
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with this email({user.email}) already exists",
            )

    # update a user
    async def update_user(self, id: UUID, user_data: UserUpdate):
        # get user by id
        user = await self._get(id)
        if not user:
            # log
            logging_service.set_log(
                message=f"User with id '{id}' doen't exist",
                log_type=LogType.ERROR,
                log_service_type=LogServiceType.DATABASE,
            )
            # raise and exception if user is not found
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with id '{id}' doen't exist",
            )

        # update users updated_at to current datetime
        user.updated_at = datetime.now()

        # log
        logging_service.set_log(
            message=f"User with id '{id}' records [[{user_data.model_dump(exclude_none=True)}]] has been updated.",
            log_type=LogType.ERROR,
            log_service_type=LogServiceType.DATABASE,
        )

        # update the user with updated data
        return await self._update(
            user.sqlmodel_update(user_data.model_dump(exclude_none=True))
        )

    # delete a user
    async def delete_user(self, id: UUID):
        # get user by id
        user = await self._get(id)
        if not user:
            # log
            logging_service.set_log(
                message=f"User with id '{id}' doen't exist",
                log_type=LogType.ERROR,
                log_service_type=LogServiceType.DATABASE,
            )
            # raise and exception if user is not found
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with id '{id}' doen't exist",
            )

        # update users deleted attribure to true
        user.deleted = True
        user.updated_at = datetime.now()
        # delete user
        await self._delete(user)

        # log
        logging_service.set_log(
            message=f"User with id '{id}' has been deleted.",
            log_type=LogType.INFO,
            log_service_type=LogServiceType.DATABASE,
        )
        return {"detail": "User deleted!"}

    # authenticate user and generate jwt token
    async def login_user(self, email: str, password: str):
        # get user with their email
        user = await self.get_user_by_email(email)

        # raise an exception if users email or password is invalid
        if not user or not password_hash.verify(password, user.password_hash):
            # log
            logging_service.set_log(
                message=f"{email} is unauthorized. Email or password is incorrect.",
                log_service_type=LogServiceType.DATABASE,
                log_type=LogType.ERROR,
            )
            # raise exception
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"{email} is unauthorized. Email or password is incorrect.",
            )

        # build dict to generate a token for authorized user
        user_data = {
            "id": str(user.id),
            "email": user.email,
        }

        # generate jwt token for the authorized user
        token = generate_jwt_token(user_data=user_data)

        if not token:
            # log
            logging_service.set_log(
                message=f"Token was not generated for {user.email}",
                log_service_type=LogServiceType.SERVICE,
                log_type=LogType.ERROR,
            )
            # raise exception
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Token was not generated for {user.email}",
            )

        # return generated jwt token
        return {
            "access_token": token,
            "token_type": "jwt",
        }
