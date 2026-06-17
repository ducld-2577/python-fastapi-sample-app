from fastapi import APIRouter, Depends

from app.api.routes import auth, comment, task, users, health, workspace, project, label
from app.core.config import get_settings
from app.core.middlewares import get_access_token

settings = get_settings()

api_router = APIRouter(prefix=settings.api_v1_prefix)

api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(
    users.router,
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(get_access_token)],
)
api_router.include_router(
    workspace.router,
    prefix="/workspaces",
    tags=["Workspaces"],
    dependencies=[Depends(get_access_token)],
)
api_router.include_router(
    project.router,
    prefix="/projects",
    tags=["Projects"],
    dependencies=[Depends(get_access_token)],
)
api_router.include_router(
    task.router,
    prefix="/tasks",
    tags=["Tasks"],
    dependencies=[Depends(get_access_token)],
)
api_router.include_router(
    label.router,
    prefix="/labels",
    tags=["Labels"],
    dependencies=[Depends(get_access_token)],
)
api_router.include_router(
    comment.router,
    prefix="/comments",
    tags=["Comments"],
    dependencies=[Depends(get_access_token)],
)
