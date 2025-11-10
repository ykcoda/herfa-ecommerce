from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database.db_session import get_db_async_session
from app.api.service.user_service import UserService
from app.api.core.security import OAUTH2_USER_SCHEMA
from app.utils import logging_service, LogServiceType, LogType

# Database Session Dependency
DB_SESSION_DEP = Annotated[AsyncSession, Depends(get_db_async_session)]


# create a UserServiceDependant
async def get_user_service(session: DB_SESSION_DEP):
    return UserService(session)


# User Service Dependency
USER_SERVICE_DEP = Annotated[UserService, Depends(get_user_service)]


# Allow Authorized users to access restricted endpoint
def get_authenticated_user(
    authenticated: Annotated[OAuth2PasswordBearer, Depends(OAUTH2_USER_SCHEMA)],
):
    if not authenticated:
        # log
        logging_service.set_log(
            "You are not authorized to access this endpoint.",
            log_service_type=LogServiceType.LOGS,
            log_type=LogType.ERROR,
        )
        # exception
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not authorized to access this endpoint.",
        )
        return False


# Authorized users Dependency
AUTHENTICATED_USER_DEP = Annotated[bool, Depends(get_authenticated_user)]
