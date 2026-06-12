from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import get_settings
from app.core.global_auth_middleware import global_auth_middleware
from app.core.lifespan import lifespan

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    debug=settings.debug,
    lifespan=lifespan,
)

app.middleware("http")(global_auth_middleware)
app.include_router(api_router)
