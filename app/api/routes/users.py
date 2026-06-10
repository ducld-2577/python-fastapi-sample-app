from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dependencies import get_access_token, get_user_service
from app.schemas.user import UserOut, UserUpdate
from app.services.user_service import UserService

router = APIRouter()


UserServiceDep = Annotated[UserService, Depends(get_user_service)]


@router.get("/me", response_model=UserOut)
async def get_user(
    service: UserServiceDep,
    token: Annotated[str, Depends(get_access_token)],
):
    return await service.get_current_user(token)


@router.patch("/me", response_model=UserOut)
async def update_user(
    payload: UserUpdate,
    service: UserServiceDep,
    token: Annotated[str, Depends(get_access_token)],
):
    return service.update_user(payload.name, token)
