from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dependencies import get_user_service
from app.schemas.user import UserOut, UserUpdate
from app.services.user_service import UserService

router = APIRouter()


UserServiceDep = Annotated[UserService, Depends(get_user_service)]


@router.get("/me", response_model=UserOut)
async def get_user(service: UserServiceDep):
    return service.get_me()


@router.patch("/me", response_model=UserOut)
async def update_user(payload: UserUpdate, service: UserServiceDep):
    return service.update_user(payload.name)
