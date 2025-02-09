from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.exc import SQLAlchemyError
from api.core.config import settings

try:
    engine = create_async_engine(settings.ASYNC_DATABASE_URL, echo=True, future=True)
except Exception as e:
    raise RuntimeError(f"Failed to initialize the database engine: {e}")

async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_async_session():
    async with async_session_maker() as session:
        try:
            yield session
        except SQLAlchemyError as e:
            print(f"Database session error: {e}")
            raise
