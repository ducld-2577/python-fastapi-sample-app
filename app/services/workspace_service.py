class WorkspaceService:

    async def create_workspace(self, name: str):
        # TODO implement create workspace logic
        return {"id": 1, "name": name}

    async def get_workspaces(self):
        # TODO implement get workspaces logic
        return [{"id": 1, "name": "Test Workspace"}]

    async def add_user_to_workspace(self, workspace_id: int, user_id: int):
        # TODO implement add user to workspace logic
        return {"message": f"User {user_id} added to workspace {workspace_id}"}

    async def remove_user_from_workspace(self, workspace_id: int, user_id: int):
        # TODO implement remove user from workspace logic
        return {"message": f"User {user_id} removed from workspace {workspace_id}"}
