import asyncio
import uuid
import pytest_asyncio
from httpx import AsyncClient
from main import app
import pytest

BASE_URL = "http://127.0.0.1:8000"


@pytest.fixture
def log_data():
    return {
        "username": "testuser",
        "password": "strongpassword123"
    }


@pytest.fixture
def user_data():
    return {
        "name": "testuser1",
        "password": "strongpassword123",
        "username": "testuser1"
    }


@pytest_asyncio.fixture
async def auth_token(client):
    name = uuid.uuid4()
    user_data = {"name": f"user_{name}", "password": "strongpassword123"}
    log_data = {"username": f"user_{name}", "password": "strongpassword123"}

    register_response = await client.post("/auth/register", json=user_data)
    if register_response.status_code != 200:
        raise ValueError("User registration failed")

    auth_response = await client.post("/auth/login", data=log_data)
    if auth_response.status_code != 200:
        raise ValueError("User registration failed")

    return auth_response.json()['access_token']


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def client():
    print("Client fixture loaded")
    return AsyncClient(base_url=BASE_URL)
