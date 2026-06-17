from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CommentCreate(BaseModel):
    task_id: int
    content: str = Field(min_length=1)

    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True,
    )


class CommentUpdate(BaseModel):
    content: str | None = Field(default=None, min_length=1)

    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True,
    )


class CommentOut(BaseModel):
    id: int
    author_id: int
    content: str
    created_at: datetime

    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True,
    )
