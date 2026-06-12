from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dependencies import get_workspace_service
from app.schemas.workspace import (
    MessageOut,
    WorkspaceCreate,
    WorkspaceMemberAdd,
    WorkspaceOut,
)
from app.services.workspace import WorkspaceService

router = APIRouter()


WorkspaceServiceDep = Annotated[WorkspaceService, Depends(get_workspace_service)]


@router.get("/", response_model=list[WorkspaceOut])
async def get_workspaces(service: WorkspaceServiceDep):
    return await service.get_workspaces()


@router.post("/", response_model=WorkspaceOut)
async def create_workspace(payload: WorkspaceCreate, service: WorkspaceServiceDep):
    return await service.create_workspace(payload.name)


@router.post("/{workspace_id}/members", response_model=MessageOut)
async def add_user_to_workspace(
    workspace_id: int,
    payload: WorkspaceMemberAdd,
    service: WorkspaceServiceDep,
):
    return await service.add_user_to_workspace(
        workspace_id,
        payload.user_id,
        payload.role,
    )


@router.delete("/{workspace_id}/members/{user_id}", response_model=MessageOut)
async def remove_user_from_workspace(
    workspace_id: int,
    user_id: int,
    service: WorkspaceServiceDep,
):
    return await service.remove_user_from_workspace(workspace_id, user_id)
