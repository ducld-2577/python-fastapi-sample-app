from typing import NoReturn

from fastapi import HTTPException, status

from app.core.security import decode_access_token
from app.models.user import User
from app.repositories.user import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def update_user(self, name: str, token: str):
        user = await self.get_current_user(token)
        user.full_name = name
        await self.user_repository.update(user)
        return {"id": user.id, "full_name": user.full_name}

    async def get_current_user(self, token: str) -> User:
        payload = decode_access_token(token)
        sub = payload.get("sub")

        if not isinstance(sub, str):
            self._raise_invalid_credentials()

        try:
            user_id = int(sub)
        except (ValueError, TypeError):
            self._raise_invalid_credentials()

        user = await self.user_repository.get(user_id)
        if user is None:
            self._raise_invalid_credentials()

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Inactive user",
            )

        return user

    @staticmethod
    def _raise_invalid_credentials() -> NoReturn:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
