from fastapi import FastAPI, APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.db.database import get_async_session

tasks_router = APIRouter(
    prefix="/task",
    tags=["tasks",'task']
)

@tasks_router.get("/")
async def tasks_list(session: AsyncSession = Depends(get_async_session)):
    taskList = await session.execute(select(Task))
    taskList = taskList.scalars().all()
    return {taskList}