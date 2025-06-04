"""API endpoints for tasks
"""
from datetime import datetime
import logging
from typing import Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from fastapi_pagination import Page, paginate
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from task_api.database import get_session
from task_api.models import Task, TaskLog
from task_api.modelschemas import TaskCreate, TaskGet, TaskUpdate
from task_api.tasks import process_task

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/",
            response_model=Page[TaskGet])
async def list_tasks(title: Optional[str] = None,
                     status: Optional[str] = None,
                     session: AsyncSession = Depends(get_session)):
    """
    Retrieve a paginated list of tasks.

    Args:
        title (Optional[str]): Filter tasks by title containing the given string.
        status (Optional[str]): Filter tasks by completion status.
        session (AsyncSession): Database session dependency.

    Returns:
        Page[TaskGet]: Paginated list of tasks.
    """

    filters = []

    if title is not None:
        filters.append(Task.title.ilike(f"%{title}%"))

    if status is not None:
        filters.append(Task.status == status)

    stmt = select(Task)

    if filters:
        stmt = stmt.where(and_(*filters))

    result = await session.execute(stmt)
    tasks = result.scalars().all()

    return paginate(tasks)


@router.get("/{task_id}/",
            response_model=TaskGet)
async def get_task(task_id: int,
                   session: AsyncSession = Depends(get_session)):
    """
    Retrieve a task by its ID.

    Args:
        task_id (int): ID of the task to retrieve.
        session (AsyncSession): Database session dependency.

    Returns:
        TaskGet: The requested task.

    Raises:
        HTTPException: If the task is not found.
    """
    task = await session.get(Task, task_id)

    if not task:
        raise HTTPException(status_code=404,
                            detail="Task not found")

    return task


@router.post("/",
             response_model=TaskGet,
             status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate,
                      background_tasks: BackgroundTasks,
                      session: AsyncSession = Depends(get_session)):
    """
    Creates and starts a new task.

    Args:
        task (TaskCreate): Task data for creation.
        background_tasks (BackgroundTasks): FastAPI background task manager.
        session (AsyncSession): Database session dependency.

    Returns:
        TaskGet: The created task object.
    """

    new_task = Task(**task.dict())
    new_task.created_at = datetime.utcnow()
    session.add(new_task)
    await session.commit()
    await session.refresh(new_task)

    task_log = TaskLog(task_id=new_task.id,
                       status=task.status)

    session.add(task_log)
    await session.commit()

    logger.info(f"A new task was created with the id: {new_task.id}")
    background_tasks.add_task(process_task, new_task.id)

    return new_task


@router.put("/{task_id}/",
            response_model=TaskGet)
async def update_task(task_id: int,
                      task_update: TaskUpdate,
                      session: AsyncSession = Depends(get_session)):
    """
    Update an existing task.

    Args:
        task_id (int): ID of the task to update.
        task_update (TaskUpdate): Updated task data.
        session (AsyncSession): Database session dependency.

    Returns:
        TaskGet: The updated task.

    Raises:
        HTTPException: If the task is not found.
    """
    task = await session.get(Task, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in task_update.dict(exclude_unset=True).items():
        setattr(task, key, value)

    session.add(task)
    await session.commit()
    await session.refresh(task)

    return task


@router.delete("/{task_id}/",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, session: AsyncSession = Depends(get_session)):
    """
    Delete a task by its ID.

    Args:
        task_id (int): ID of the task to delete.
        session (AsyncSession): Database session dependency.

    Returns:
        None

    Raises:
        HTTPException: If the task is not found.
    """
    task = await session.get(Task, task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    await session.delete(task)
    await session.commit()

    return
