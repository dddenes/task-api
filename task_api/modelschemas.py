"""Modelschemas to represent DB objects
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TaskBase(BaseModel):
    """Modelschema used as a parent for more specific schemas
    """
    title: str
    description: Optional[str] = None
    status: str
    priority: int


class TaskGet(TaskBase):
    """Modelschema used for getting tasks
    """
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }


class TaskCreate(TaskBase):
    """Modelschema used for creating new tasks
    """
    pass


class TaskUpdate(BaseModel):
    """Modelschema used for updating already existing tasks
    """
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[int] = None


class TaskLogGet(BaseModel):
    """Modelschema used for getting task logs
    """
    id: int
    task_id: int
    status: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
