from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dependencies import (
    get_project_service,
)

from app.schemas.project import ProjectCreate, ProjectRead, ProjectUpdate
from app.services.project import ProjectService

router = APIRouter()

ProjectServiceDep = Annotated[ProjectService, Depends(get_project_service)]


@router.get("/{project_id}", response_model=ProjectRead)
async def get_project(
    project_id: int,
    service: ProjectServiceDep,
):
    return await service.get_project(project_id)


@router.get("/workspace/{workspace_id}", response_model=list[ProjectRead])
async def get_projects_by_workspace(
    workspace_id: int,
    service: ProjectServiceDep,
):
    return await service.get_projects_by_workspace(workspace_id)


@router.delete("/{project_id}")
async def delete_project(
    project_id: int,
    service: ProjectServiceDep,
):
    return await service.delete_project(project_id)


@router.post("/", response_model=ProjectRead)
async def create_project(
    payload: ProjectCreate,
    service: ProjectServiceDep,
):
    return await service.create_project(payload)


@router.put("/{project_id}", response_model=ProjectRead)
async def update_project(
    project_id: int,
    payload: ProjectUpdate,
    service: ProjectServiceDep,
):
    return await service.update_project(project_id, payload)


@router.post("/{project_id}/archive", response_model=ProjectRead)
async def archive_project(
    project_id: int,
    service: ProjectServiceDep,
):
    return await service.archive_project(project_id)
