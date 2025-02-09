from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from api.db.database import get_async_session
from api.db.models import User
from api.schemas.auth_schemas import UserCreate, UserOut, UserDB, UserOutList
from starlette import status

from .utils import get_password_hash, verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.get("/list", response_model=list[UserOutList])
async def tasks_list(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(User))
    task_list = result.scalars().all()
    return task_list


@auth_router.post("/register", response_model=UserOut)
async def register_user(user: UserCreate, session: AsyncSession = Depends(get_async_session)):
    query = select(User).where(User.name == user.name)
    existing_user = (await session.execute(query)).scalars().first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    hashed_password = get_password_hash(user.password)
    new_user = User(name=user.name, hashed_password=hashed_password)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


@auth_router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_async_session)):
    query = select(User).where(User.name == form_data.username)
    user = (await session.execute(query)).scalars().first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = create_access_token(data={"sub": user.name})
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.delete("/delete_user/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(
        user_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    query = select(User).where(User.id == user_id)
    result = await session.execute(query)
    task = result.scalar_one_or_none()

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {user_id} not found.",
        )
    await session.delete(task)
    await session.commit()
    return {"message": f"Task {user_id} deleted successfully."}
