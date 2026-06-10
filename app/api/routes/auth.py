from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dependencies import get_auth_service
from app.schemas.auth import RefreshTokenPayload, UserLoginPayload, UserRegisterPayload
from app.services.auth_service import AuthService

router = APIRouter()


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


@router.post("/register")
async def register(service: AuthServiceDep, payload: UserRegisterPayload):
    return await service.register(payload)


@router.post("/login")
async def login(service: AuthServiceDep, payload: UserLoginPayload):
    return await service.login(payload)


@router.post("/refresh")
async def refresh_token(service: AuthServiceDep, payload: RefreshTokenPayload):
    return await service.refresh_access_token(payload.refresh_token)


@router.post("/logout")
async def logout(
    service: AuthServiceDep,
):
    return await service.logout()
