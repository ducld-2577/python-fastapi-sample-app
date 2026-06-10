from fastapi import APIRouter
from app.api.routes import auth, users, health, workspace
from app.core.config import get_settings

settings = get_settings()

api_router = APIRouter(prefix=settings.api_v1_prefix)

api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(workspace.router, prefix="/workspaces", tags=["Workspaces"])
