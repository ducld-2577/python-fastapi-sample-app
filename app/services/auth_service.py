from fastapi import HTTPException, status

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    hash_password,
    verify_password,
)
from app.repositories.user import UserRepository
from app.schemas.auth import UserLoginPayload, UserRegisterPayload


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def register(self, payload: UserRegisterPayload):
        try:
            is_email_exist = await self.verify_email(payload.email)
            if is_email_exist:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already exists",
                )

            hashed = hash_password(payload.password)

            return await self.user_repository.create_user(
                email=payload.email,
                full_name=payload.full_name,
                hashed_password=hashed,
            )
        except Exception:
            raise

    async def verify_email(self, email: str):
        try:
            user = await self.user_repository.get_by_email(email)
            return user is not None
        except Exception:
            raise

    async def login(self, payload: UserLoginPayload):
        try:
            user = await self.user_repository.get_by_email(payload.email)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid email or password",
                )

            if not verify_password(payload.password, user.hashed_password):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid email or password",
                )

            if not user.is_active:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Inactive user",
                )

            access_token = create_access_token(user.id)
            refresh_token = create_refresh_token(user.id)

            return {
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "full_name": user.full_name,
                },
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
            }
        except Exception:
            raise

    async def refresh_access_token(self, refresh_token: str):
        payload = decode_refresh_token(refresh_token)
        sub = payload.get("sub")

        if not isinstance(sub, str):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        try:
            user_id = int(sub)
        except (ValueError, TypeError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user = await self.user_repository.get(user_id)
        if user is None or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = create_access_token(user.id)
        return {"access_token": access_token, "token_type": "bearer"}

    async def logout(self):
        return {
            "message": "Logout successful. Please delete the token on the client side."
        }
