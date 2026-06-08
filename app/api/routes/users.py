from fastapi import APIRouter, Depends
from app.services.user_service import UserService

router = APIRouter()


def get_user_service():
    return UserService()


@router.get("/me")
async def get_user(service: UserService = Depends(get_user_service)):
    return service.get_me()


@router.patch("/me")
async def update_user(user: dict, service: UserService = Depends(get_user_service)):
    return service.update_user(user)
