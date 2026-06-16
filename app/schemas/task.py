from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from app.models.task import TaskPriority, TaskStatus


class TaskCreate(BaseModel):
    project_id: int
    assignee_id: int | None = None
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None)
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: datetime | None = None


class TaskUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=500)


class TaskAssign(BaseModel):
    assignee_id: int


class TaskUpdateStatus(BaseModel):
    status: TaskStatus


class TaskUpdatePriority(BaseModel):
    priority: TaskPriority


class TaskRead(BaseModel):
    id: int
    project_id: int
    assignee_id: int | None
    title: str
    description: str | None
    status: TaskStatus
    priority: TaskPriority
    due_date: datetime | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
