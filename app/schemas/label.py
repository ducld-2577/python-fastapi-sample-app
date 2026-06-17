from pydantic import BaseModel, ConfigDict, Field


class LabelCreate(BaseModel):
    project_id: int
    name: str = Field(min_length=1, max_length=255)
    color: str = Field(min_length=1, max_length=7)  # Hex color code

    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True,
    )


class LabelUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    color: str | None = Field(
        default=None, min_length=1, max_length=7
    )  # Hex color code

    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True,
    )


class LabelAssignTask(BaseModel):
    task_id: int
    label_id: int

    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True,
    )
