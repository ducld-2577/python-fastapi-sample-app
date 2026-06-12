from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.config import get_settings
from app.db.redis import create_redis_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("App starting...")

    settings = get_settings()
    app.state.redis = create_redis_client(settings.redis_url)
    await app.state.redis.ping()

    yield

    await app.state.redis.aclose()

    print("App shutting down...")
