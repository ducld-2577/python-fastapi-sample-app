from datetime import datetime
from pydantic import BaseModel
from app.models.workspace import WorkspaceMemberRole


class WorkspaceCreate(BaseModel):
    name: str


class WorkspaceMemberAdd(BaseModel):
    user_id: int
    role: WorkspaceMemberRole


class MessageOut(BaseModel):
    message: str


class WorkspaceOut(BaseModel):
    id: int
    name: str
    owner_id: int
    created_at: datetime | None = None

    model_config = {"from_attributes": True}
