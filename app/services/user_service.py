from app.repositories.user import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_me(self):
        # TODO: Implement actual logic to get user information from the database
        return {"id": 1, "name": "test user"}

    def update_user(self, name: str):
        # TODO: Implement actual logic to update user information in the database
        return {"id": 1, "name": name}
