from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dependencies import (
    get_user_service,
    CurrentUser,
)
from app.schemas.user import UserOut, UserUpdate
from app.services.user import UserService

router = APIRouter()

UserServiceDep = Annotated[UserService, Depends(get_user_service)]


@router.get("/me", response_model=UserOut)
async def get_current_user_profile(
    current_user: CurrentUser,
):
    return current_user


@router.patch("/me", response_model=UserOut)
async def update_user(
    payload: UserUpdate,
    current_user: CurrentUser,
    service: UserServiceDep,
):
    return await service.update_user(payload.name, current_user.id)
