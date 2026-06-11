from fastapi import HTTPException
from starlette import status

from app.models.project import Project, ProjectStatus
from app.repositories.project import ProjectRepository
from app.repositories.workspace import WorkspaceRepository
from app.schemas.project import ProjectCreate, ProjectUpdate


class ProjectService:
    def __init__(
        self,
        project_repository: ProjectRepository,
        workspace_repository: WorkspaceRepository,
    ):
        self.project_repository = project_repository
        self.workspace_repository = workspace_repository

    async def create_project(self, payload: ProjectCreate):
        workspace = await self.workspace_repository.get_by_id(payload.workspace_id)
        if not workspace:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Workspace not found",
            )

        project = Project(
            workspace_id=payload.workspace_id,
            name=payload.name,
            description=payload.description,
        )
        return await self.project_repository.create(project)

    async def get_project(self, project_id):
        project = await self.project_repository.get(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )
        return project

    async def get_projects_by_workspace(self, workspace_id):
        workspace = await self.workspace_repository.get_by_id(workspace_id)
        if not workspace:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Workspace not found",
            )
        return await self.project_repository.get_projects_by_workspace(workspace_id)

    async def delete_project(self, project_id):
        project = await self.project_repository.get(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )
        await self.project_repository.delete(project_id)
        return {"message": f"Project {project_id} deleted successfully"}

    async def update_project(self, project_id, payload: ProjectUpdate):
        project = await self.project_repository.get(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )
        project.name = payload.name
        project.description = payload.description
        return await self.project_repository.update(project)

    async def archive_project(self, project_id):
        project = await self.project_repository.get(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )
        project.status = ProjectStatus.ARCHIVED
        return await self.project_repository.update(project)
