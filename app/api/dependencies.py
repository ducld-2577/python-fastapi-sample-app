from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.user import User
from app.repositories.user import UserRepository
from app.repositories.workspace import WorkspaceRepository
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.services.workspace_service import WorkspaceService

DbSession = Annotated[AsyncSession, Depends(get_db)]
bearer_scheme = HTTPBearer()


def get_access_token(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
) -> str:
    return credentials.credentials


def get_user_repository(db: DbSession) -> UserRepository:
    return UserRepository(db)


def get_workspace_repository(db: DbSession) -> WorkspaceRepository:
    return WorkspaceRepository(db)


def get_auth_service(
    repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> AuthService:
    return AuthService(repository)


def get_user_service(
    repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> UserService:
    return UserService(repository)


def get_workspace_service(
    repository: Annotated[WorkspaceRepository, Depends(get_workspace_repository)],
) -> WorkspaceService:
    return WorkspaceService(repository)
