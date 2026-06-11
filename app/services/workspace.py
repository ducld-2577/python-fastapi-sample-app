from app.models.workspace import Workspace, WorkspaceMemberRole
from app.repositories.workspace import WorkspaceRepository


class WorkspaceService:
    def __init__(self, workspace_repository: WorkspaceRepository):
        self.workspace_repository = workspace_repository

    async def create_workspace(self, name: str):
        # TODO: get user id from auth token
        owner_id = 1
        workspace = Workspace(name=name, owner_id=owner_id)
        return await self.workspace_repository.create(workspace)

    async def get_workspaces(self):
        # TODO: get user id from auth token
        owner_id = 1

        # TODO: pagination
        return await self.workspace_repository.get_workspaces(owner_id)

    async def add_user_to_workspace(
        self, workspace_id: int, user_id: int, role: WorkspaceMemberRole
    ):
        await self.workspace_repository.add_member_into_workspace(
            workspace_id, user_id, role
        )
        return {"message": f"User {user_id} added to workspace {workspace_id}"}

    async def remove_user_from_workspace(self, workspace_id: int, user_id: int):
        await self.workspace_repository.remove_member_from_workspace(
            workspace_id, user_id
        )
        return {"message": f"User {user_id} removed from workspace {workspace_id}"}
