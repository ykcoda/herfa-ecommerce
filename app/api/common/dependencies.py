from typing import Annotated
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from app.database.db_session import get_db_async_session


# Creates a dependency for Database session
DB_SESSION_DEP = Annotated[AsyncSession, Depends(get_db_async_session)]
