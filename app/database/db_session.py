from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from app.config import database_settings

# create async db engine
async_engine = create_async_engine(url=database_settings.DB_URL, echo=False)


# get db async session for db activities
async def get_db_async_session():

    # create sessionmaker
    async_session = sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    # yields async session
    async with async_session() as session:
        yield session
