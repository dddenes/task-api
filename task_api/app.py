"""Application factory
"""

import logging

from fastapi import FastAPI
from fastapi_pagination import add_pagination

from task_api.routers import tasks, task_logs

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    logger.info('Starting of the Task API app...')

    app = FastAPI(title="Task API")
    app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
    app.include_router(task_logs.router, prefix="/task-logs", tags=["Task logs"])
    add_pagination(app)

    return app
