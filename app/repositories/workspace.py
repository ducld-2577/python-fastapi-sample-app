from app.repositories.base import BaseRepository
from app.models.workspace import Workspace, WorkspaceMember, WorkspaceMemberRole


class WorkspaceRepository(BaseRepository[Workspace]):
    def __init__(self, session):
        super().__init__(Workspace, session)

    async def get_by_id(self, workspace_id: int) -> Workspace | None:
        from sqlalchemy import select

        result = await self.session.execute(
            select(Workspace).where(Workspace.id == workspace_id)
        )
        return result.scalar_one_or_none()

    async def get_workspaces(self, owner_id: int):
        from sqlalchemy import select

        result = await self.session.execute(
            select(Workspace).where(Workspace.owner_id == owner_id)
        )
        return result.scalars().all()

    async def get_membership(
        self, workspace_id: int, user_id: int
    ) -> WorkspaceMember | None:
        from sqlalchemy import select
        from sqlalchemy.orm import selectinload

        result = await self.session.execute(
            select(WorkspaceMember)
            .options(selectinload(WorkspaceMember.user))
            .where(
                WorkspaceMember.workspace_id == workspace_id,
                WorkspaceMember.user_id == user_id,
            )
        )
        return result.scalar_one_or_none()

    async def add_member_into_workspace(
        self, workspace_id: int, user_id: int, role: WorkspaceMemberRole
    ) -> None:
        from sqlalchemy import insert

        stmt = insert(WorkspaceMember).values(
            workspace_id=workspace_id,
            user_id=user_id,
            role=role,
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def remove_member_from_workspace(
        self, workspace_id: int, user_id: int
    ) -> None:
        from sqlalchemy import delete

        stmt = delete(WorkspaceMember).where(
            WorkspaceMember.workspace_id == workspace_id,
            WorkspaceMember.user_id == user_id,
        )
        await self.session.execute(stmt)
        await self.session.commit()
