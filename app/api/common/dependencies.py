from typing import Annotated
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from app.database.db_session import get_db_async_session
from app.api.service.user_service import UserService


# Database Session Dependency
DB_SESSION_DEP = Annotated[AsyncSession, Depends(get_db_async_session)]


# create a UserServiceDependant
async def get_user_service(session: DB_SESSION_DEP):
    return UserService(session)


# User Service Dependency
USER_SERVICE_DEP = Annotated[UserService, Depends(get_user_service)]
