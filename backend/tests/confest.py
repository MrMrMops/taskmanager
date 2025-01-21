import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from api.db.database import get_async_session, Base
from backend.main import app

# Настройки для тестовой базы данных
DATABASE_URL = "sqlite+aiosqlite:///./test.db"
engine = create_async_engine(DATABASE_URL, future=True)
TestSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Фикстура для базы данных
@pytest.fixture(scope="function", autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

# Фикстура для замены зависимости get_async_session
@pytest.fixture(scope="function")
def override_get_db():
    async def get_db_override():
        async with TestSessionLocal() as session:
            yield session

    app.dependency_overrides[get_async_session] = get_db_override

# Фикстура для клиента
@pytest.fixture(scope="function")
async def client(override_get_db):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac