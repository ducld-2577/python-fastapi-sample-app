from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dependencies import (
    get_comment_service,
)

from app.core.middlewares import get_current_user
from app.models.user import User
from app.schemas.comment import CommentCreate, CommentOut, CommentOut, CommentUpdate
from app.services.comment import CommentService

router = APIRouter()

CommentServiceDep = Annotated[CommentService, Depends(get_comment_service)]


@router.get("/task/{task_id}", response_model=list[CommentOut])
async def get_comments_by_task(
    task_id: int,
    service: CommentServiceDep,
    page: int = 1,
    page_size: int = 10,
):
    return await service.get_comments_by_task(
        task_id=task_id,
        limit=page_size,
        page=page,
    )


@router.get("/{user_id}", response_model=list[CommentOut])
async def get_comments_by_user(
    user_id: int,
    service: CommentServiceDep,
    page: int = 1,
    page_size: int = 10,
):
    return await service.get_comments_by_author(
        author_id=user_id,
        limit=page_size,
        page=page,
    )


@router.post("/", response_model=CommentOut)
async def create_comment(
    payload: CommentCreate,
    service: CommentServiceDep,
    current_user: Annotated[User, Depends(get_current_user)],
):
    return await service.create_comment(current_user.id, payload)


@router.put("/{comment_id}", response_model=CommentOut)
async def update_comment(
    comment_id: int,
    payload: CommentUpdate,
    service: CommentServiceDep,
    current_user: Annotated[User, Depends(get_current_user)],
):
    return await service.update_comment(comment_id, current_user.id, payload)


@router.delete("/{comment_id}")
async def delete_comment(
    comment_id: int,
    service: CommentServiceDep,
    current_user: Annotated[User, Depends(get_current_user)],
):
    await service.delete_comment(comment_id, current_user.id)
    return {"detail": "Comment deleted successfully"}
