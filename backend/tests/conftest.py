import asyncio

import pytest
import pytest_asyncio
from fastapi import Depends
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from main import app
from api.db.database import get_async_session, Base
import pytest

# SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"
#
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )
# class Base(DeclarativeBase): pass
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#
# Base.metadata.create_all(bind=engine)
#
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
def client():
    print("Client fixture loaded")
    return AsyncClient()