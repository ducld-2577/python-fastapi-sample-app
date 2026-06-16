from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from app.models.project import ProjectStatus
from app.models.task import TaskPriority


class LabelCreate(BaseModel):
    project_id: int
    name: str = Field(min_length=1, max_length=255)
    color: str = Field(min_length=1, max_length=7)  # Hex color code

    model_config = ConfigDict(
        extra="forbid",
    )


class LabelUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    color: str | None = Field(
        default=None, min_length=1, max_length=7
    )  # Hex color code

    model_config = ConfigDict(
        extra="forbid",
    )


class LabelAssignTask(BaseModel):
    task_id: int
    label_id: int

    model_config = ConfigDict(
        extra="forbid",
    )
