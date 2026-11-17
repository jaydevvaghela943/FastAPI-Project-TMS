from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

TaskStatus = Literal[
    "todo",
    "in_progress",
    "review",
    "completed"
]

TaskPriority = Literal[
    "low",
    "medium",
    "high",
    "urgent"
]


# Create task
class TaskCreate(BaseModel):

    title: str = Field(
        min_length=2,
        max_length=200
    )

    description: str | None = None
    status: TaskStatus = "todo"
    priority: TaskPriority = "medium"
    due_date: datetime | None = None
    project_id: int

# Update task
class TaskUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=2,
        max_length=200
    )

    description: str | None = None
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    due_date: datetime | None = None
    assigned_to: int | None = None
    model_config = ConfigDict(extra="forbid")


# Task response
class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: TaskStatus
    priority: TaskPriority
    due_date: datetime | None
    project_id: int
    assigned_to: int | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class TaskList(BaseModel):
    items: list[TaskResponse]
    total: int
    page: int
    size: int

class TaskStatusUpdate(BaseModel):
    status: TaskStatus

class ProjectTaskCreate(BaseModel):
    title: str = Field(
        min_length=2,
        max_length=200
    )
    description: str | None = None
    status: TaskStatus = "todo"
    priority: TaskPriority = "medium"
    due_date: datetime | None = None
    