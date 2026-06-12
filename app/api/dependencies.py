from typing import Annotated

from fastapi import Depends, Request
from app.repositories.task import TaskRepository
from app.services.task import TaskService
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.middlewares import get_current_user, require_admin
from app.db.redis import get_redis_from_request
from app.db.session import get_db
from app.models.user import User
from app.repositories.project import ProjectRepository
from app.repositories.user import UserRepository
from app.repositories.workspace import WorkspaceRepository
from app.services.auth import AuthService
from app.services.project import ProjectService
from app.services.user import UserService
from app.services.workspace import WorkspaceService

DbSession = Annotated[AsyncSession, Depends(get_db)]


def get_redis(request: Request) -> Redis:
    return get_redis_from_request(request)


def get_user_repository(db: DbSession) -> UserRepository:
    return UserRepository(db)


def get_workspace_repository(db: DbSession) -> WorkspaceRepository:
    return WorkspaceRepository(db)


def get_project_repository(db: DbSession) -> ProjectRepository:
    return ProjectRepository(db)


def get_task_repository(db: DbSession) -> TaskRepository:
    return TaskRepository(db)


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


def get_project_service(
    project_repository: Annotated[ProjectRepository, Depends(get_project_repository)],
    workspace_repository: Annotated[
        WorkspaceRepository, Depends(get_workspace_repository)
    ],
) -> ProjectService:
    return ProjectService(project_repository, workspace_repository)


def get_task_service(
    task_repository: Annotated[TaskRepository, Depends(get_task_repository)],
    project_repository: Annotated[ProjectRepository, Depends(get_project_repository)],
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> TaskService:
    return TaskService(
        task_repository,
        user_repository,
        project_repository,
    )


CurrentUser = Annotated[User, Depends(get_current_user)]
RequireAdmin = Annotated[User, Depends(require_admin)]
