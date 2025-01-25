import logging
import uuid
from datetime import datetime
from typing import Dict, Any

from fastapi import FastAPI, APIRouter, Depends, HTTPException
from pydantic import HttpUrl
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from api.db.database import get_async_session
from api.db.models import Task, User
from api.schemas.tasks_schemas import TaskCreate, TaskUpdate
from api.schemas.tasks_schemas import Task as task
from starlette import status
from .utils import get_current_user


tasks_router = APIRouter(
    prefix="/task",
    tags=["tasks",'task']
)

logger = logging.getLogger(__name__)

@tasks_router.get("/list", response_model=list[task])
async def tasks_list(session: AsyncSession = Depends(get_async_session)):#,user: User = Depends(get_current_user)):
    result = await session.execute(select(Task))
    task_list = result.scalars().all()
    return task_list

@tasks_router.post("/create_task", status_code=status.HTTP_201_CREATED)
async def task_create(
    task: TaskCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(get_current_user)
):


# Создание объекта задачи
    new_task = Task(
        title=task.title,
        text=task.text,
        image_url=task.image_url,
        due_date=task.due_date,
        priority=task.priority,
    )

    session.add(new_task)
    try:
        await session.commit()
        await session.refresh(new_task)
        logger.info(f"Task created successfully: {new_task.id}")

    except IntegrityError as e:
        logger.error(f"Integrity error during task creation: {e}")
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Integrity error: Check if the provided data is correct.",
        )
    except SQLAlchemyError as e:
        logger.error(f"Database error during task creation: {e}")
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred. Please try again later.",
        )
    except Exception as e:
        logger.critical(f"Unexpected error during task creation: {e}")
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error occurred. Please contact support.",
        )

    # Возвращение успешного ответа
    return {
        "message": "Task created successfully",
        "task": {
            "id": new_task.id,
            "title": new_task.title,
            "priority": new_task.priority,
            "created_date": new_task.created_date,
            "updated_date": new_task.updated_date,
        },
    }
@tasks_router.delete("/delete_task/{task_id}", status_code=status.HTTP_200_OK)
async def delete_task(
    task_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        # Проверка существования задачи
        query = select(Task).where(Task.id == task_id)
        result = await session.execute(query)
        task = result.scalar_one_or_none()

        if task is None:
            logger.warning(f"Task with ID {task_id} not found.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with ID {task_id} not found.",
            )

        # Удаление задачи
        await session.delete(task)
        await session.commit()
        logger.info(f"Task {task_id} deleted successfully.")
        return {"message": f"Task {task_id} deleted successfully."}

    except SQLAlchemyError as e:
        logger.error(f"Database error during task deletion: {e}")
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred. Please try again later.",
        )
    except Exception as e:
        logger.critical(f"Unexpected error during task deletion: {e}")
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error occurred. Please contact support.",
        )

@tasks_router.put("/update_task/{task_id}", status_code=status.HTTP_200_OK)
async def update_task(
        task_id:int,
        task_update: TaskUpdate,
        session: AsyncSession = Depends(get_async_session),
):

    try:
        query = select(Task).where(Task.id == task_id)
        result = await session.execute(query)

        task = result.scalar_one_or_none()

        if task is None:
            logger.warning(f"Task with ID {task_id} not found.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with ID {task_id} not found.",
            )

        # Применение изменений
        update_data: Dict[str, Any] = task_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        # Обновление времени изменения
        task.updated_date = datetime.utcnow()

        # Сохранение изменений
        await session.commit()
        await session.refresh(task)
        logger.info(f"Task {task_id} updated successfully.")

        return {"message": f"Task {task_id} updated successfully.", "task": task}

    except SQLAlchemyError as e:
        logger.error(f"Database error during task update: {e}")
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred. Please try again later.",
        )
    except Exception as e:
        logger.critical(f"Unexpected error during task update: {e}")
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error occurred. Please contact support.",
        )