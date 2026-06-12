from app.repositories.base import BaseRepository
from app.models.project import Project, ProjectStatus


class ProjectRepository(BaseRepository):
    def __init__(self, session):
        from app.models.project import Project

        super().__init__(Project, session)

    async def archive_project(self, project_id: int):
        from sqlalchemy import update

        await self.session.execute(
            update(Project)
            .where(Project.id == project_id)
            .values(status=ProjectStatus.ARCHIVED)
        )
        await self.session.commit()

    async def get_projects_by_workspace(self, workspace_id: int):
        from sqlalchemy import select

        result = await self.session.execute(
            select(Project).where(Project.workspace_id == workspace_id)
        )
        return result.scalars().all()
