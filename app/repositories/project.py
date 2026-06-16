from app.repositories.base import BaseRepository
from app.models.project import Project, ProjectStatus
from sqlalchemy import select, update


class ProjectRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(Project, session)

    async def archive_project(self, project_id: int):
        await self.session.execute(
            update(Project)
            .where(Project.id == project_id)
            .values(status=ProjectStatus.ARCHIVED)
        )
        await self.session.commit()

    async def get_projects_by_workspace(
        self,
        workspace_id: int,
        limit: int = 10,
        offset: int = 0,
    ):
        result = await self.session.execute(
            select(Project)
            .where(Project.workspace_id == workspace_id)
            .order_by(Project.id.desc())
            .limit(limit)
            .offset(offset)
        )
        return result.scalars().all()
