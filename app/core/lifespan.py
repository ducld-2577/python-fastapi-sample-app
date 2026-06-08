from contextlib import asynccontextmanager
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("App starting...")

    # TODO connect DB
    yield

    print("App shutting down...")
