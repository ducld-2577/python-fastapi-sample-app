"""Authentication and authorization dependencies."""

from typing import Annotated, Optional

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.user import User, UserRole
from app.repositories.user import UserRepository

bearer_scheme = HTTPBearer()


def get_access_token(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
) -> str:
    return credentials.credentials


async def get_current_user(
    request: Request,
    token: Annotated[str, Depends(get_access_token)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    cached_user = getattr(request.state, "current_user", None)
    if cached_user is not None:
        return cached_user

    try:
        payload = decode_access_token(token)
        sub = payload.get("sub")
        if sub is None:
            raise KeyError("sub not found in token")
        user_id = int(sub)
    except (ValueError, KeyError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_repo = UserRepository(db)
    user = await user_repo.get(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    request.state.current_user = user

    return user


async def require_admin(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admin role required.",
        )
    return current_user


async def require_admin_or_owner(
    current_user: Annotated[User, Depends(get_current_user)],
    resource_owner_id: Optional[int] = None,
) -> User:
    if current_user.role == UserRole.ADMIN:
        return current_user

    if resource_owner_id is not None and current_user.id == resource_owner_id:
        return current_user

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Access denied. Admin or owner access required.",
    )
