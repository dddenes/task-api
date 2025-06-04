"""API endpoints for task_logs
"""

from fastapi import APIRouter, Depends
from fastapi_pagination import Page, paginate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from task_api.database import get_session
from task_api.models import TaskLog
from task_api.modelschemas import TaskLogGet

router = APIRouter()


@router.get("/",
            response_model=Page[TaskLogGet])
async def read_task_logs(session: AsyncSession = Depends(get_session)):
    """
    Retrieve a paginated list of task_logs.

    Args:
        session (AsyncSession): Database session dependency.

    Returns:
        Page[TaskLogGet]: Paginated list of tasks.
    """

    logs = await session.execute(select(TaskLog))
    logs = logs.scalars().all()

    return paginate(logs)
