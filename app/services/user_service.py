class UserService:
    def get_me(self):
        return {"id": 1, "name": "test user"}

    def update_user(self, user: dict):
        return {"id": 1, "name": user.get("name", "test user")}
