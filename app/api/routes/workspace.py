from fastapi import APIRouter, Depends
from app.services.workspace_service import WorkspaceService

router = APIRouter()


def get_workspace_service():
    return WorkspaceService()


@router.get("/")
async def get_workspaces(service: WorkspaceService = Depends(get_workspace_service)):
    return await service.get_workspaces()


@router.post("/")
async def create_workspace(
    name: str, service: WorkspaceService = Depends(get_workspace_service)
):
    return await service.create_workspace(name)


@router.post("/{workspace_id}/members")
async def add_user_to_workspace(
    workspace_id: int,
    user_id: int,
    service: WorkspaceService = Depends(get_workspace_service),
):
    return await service.add_user_to_workspace(workspace_id, user_id)


@router.delete("/{workspace_id}/members/{user_id}")
async def remove_user_from_workspace(
    workspace_id: int,
    user_id: int,
    service: WorkspaceService = Depends(get_workspace_service),
):
    return await service.remove_user_from_workspace(workspace_id, user_id)
