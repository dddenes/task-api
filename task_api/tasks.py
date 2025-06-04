"""Backround tasks to run
"""
import logging
from functools import wraps

import asyncio

logger = logging.getLogger(__name__)


def background_task_wrapper(func):
    """Wrapper for background task errorhandling"""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            await func(*args, **kwargs)
            print(args[0])
        except Exception as e:
            logger.exception(f"Exception in background task {func.__name__} task_id: {args[0]}: {e}")

    return wrapper


@background_task_wrapper
async def process_task(task_id: int):
    """A sample background task to run"""

    print(f'Processing task {task_id}')

    await asyncio.sleep(5)
