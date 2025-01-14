from datetime import datetime

from fastapi import FastAPI, APIRouter, Depends
from pydantic import HttpUrl
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from api.db.database import get_async_session
from api.db.models import Task
from api.schemas.tasks_schemas import Task as task

tasks_router = APIRouter(
    prefix="/task",
    tags=["tasks",'task']
)

@tasks_router.get("/list", response_model=list[task])
async def tasks_list(priority: int, due_date: datetime,image_url: HttpUrl,text: str,title:str,session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Task))
    task_list = result.scalars().all()
    return task_list

# @tasks_router.get("/create_task")
# async def task_create(session: AsyncSession = Depends(get_async_session)):
