from typing import Annotated
from fastapi import Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database.db_session import get_db_async_session
from app.api.service.user_service import UserService
from app.api.core.security import OAUTH2_USER_SCHEMA
from app.utils import (
    decode_encoded_jwt_token,
    logging_service,
    LogServiceType,
    LogType,
    redis_service,
)
from app.api.service.category_service import CategoryService

# Database Session Dependency
DB_SESSION_DEP = Annotated[AsyncSession, Depends(get_db_async_session)]


# create a UserServiceDependant
async def get_user_service(session: DB_SESSION_DEP):
    return UserService(session)


# User Service Dependency
USER_SERVICE_DEP = Annotated[UserService, Depends(get_user_service)]


# create a CategoryServiceDependant
async def get_category_service(session: DB_SESSION_DEP):
    return CategoryService(session)


# Category Service Dependency
CATEGORY_SERVICE_DEP = Annotated[CategoryService, Depends(get_category_service)]


# Allow Authorized users to access restricted endpoint
async def get_authenticated_user(
    authenticated: Annotated[str, Depends(OAUTH2_USER_SCHEMA)],
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
        return None

    # decode encoded token
    decoded_token = decode_encoded_jwt_token(authenticated)

    # if token is not decoded or if user is logged out of the system
    if not decoded_token or await redis_service.jti_exists(decoded_token["jti"]):
        # log
        logging_service.set_log(
            "Unauthorized access or access token has expired",
            log_service_type=LogServiceType.LOGS,
            log_type=LogType.ERROR,
        )
        # exception
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized or access token has expired",
        )

    return decoded_token


# Authorized users Dependency
AUTHENTICATED_USER_DEP = Annotated[bool, Depends(get_authenticated_user)]
