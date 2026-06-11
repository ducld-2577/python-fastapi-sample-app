from fastapi import HTTPException, status

from app.models.user import User
from app.repositories.user import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def update_user(self, name: str, user_id: int) -> User:
        user = await self.user_repository.get(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        user.full_name = name
        return await self.user_repository.update(user)
