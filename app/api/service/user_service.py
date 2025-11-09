from fastapi import HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.database.model.user import User
from app.api.service.base_service import BaseService
from app.database.schemas.user import UserCreate, UserUpdate
from datetime import datetime
from uuid import UUID

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

    # create a user
    async def create_user(self, user: UserCreate):
        # check if email exists in uses table
        if not await self.get_user_by_email(user.email):
            # only create user if the email is not present in users table
            new_user = User(
                **user.model_dump(), password_hash=password_hash.hash(user.password)
            )
            return await self._create(new_user)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists",
            )

    # update a user
    async def update_user(self, id: UUID, user_data: UserUpdate):
        # get user by id
        user = await self._get(id)
        if not user:
            # raise and exception if user is not found
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User doesn't exists!"
            )

        # update users updated_at to current datetime
        user.updated_at = datetime.now()

        # update the user with updated data
        return await self._update(
            user.sqlmodel_update(user_data.model_dump(exclude_none=True))
        )

    # delete a user
    async def delete_user(self, id: UUID):
        # get user by id
        user = await self._get(id)
        if not user:
            # raise and exception if user is not found
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User doesn't exists!"
            )
        # delete user
        await self._delete(user)

        return {"detail": "User deleted!"}
