"""Classes for DB models
"""

from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, Text, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Task(Base):
    """Class for tasks DB model
    """
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(String(50), nullable=False)
    priority = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class TaskLog(Base):
    """Class for task_logs DB model
    """
    __tablename__ = "task_logs"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    status = Column(String(50), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow, nullable=False)
