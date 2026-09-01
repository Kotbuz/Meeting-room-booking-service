from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine(settings.database_url, echo=settings.debug,)

new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with new_session() as session:
        yield session


class Base(DeclarativeBase):
    pass
