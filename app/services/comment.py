from fastapi import HTTPException
from starlette import status

from app.models.comment import Comment
from app.repositories.comment import CommentRepository
from app.repositories.task import TaskRepository
from app.repositories.user import UserRepository
from app.schemas.comment import CommentCreate, CommentUpdate


class CommentService:
    def __init__(
        self,
        comment_repository: CommentRepository,
        task_repository: TaskRepository,
        user_repository: UserRepository,
    ):
        self.comment_repository = comment_repository
        self.task_repository = task_repository
        self.user_repository = user_repository

    async def create_comment(self, current_user_id: int, payload: CommentCreate):
        task = await self.task_repository.get(payload.task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        print(f"current_user_id{current_user_id}")

        user = await self.user_repository.get(current_user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        comment = Comment(
            task_id=payload.task_id,
            author_id=current_user_id,
            content=payload.content,
        )
        return await self.comment_repository.create(comment)

    async def update_comment(
        self, comment_id: int, current_user_id: int, payload: CommentUpdate
    ):
        comment = await self.comment_repository.get(comment_id)
        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment not found",
            )

        if comment.author_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to update this comment",
            )

        comment.content = payload.content
        return await self.comment_repository.update(comment)

    async def delete_comment(self, comment_id: int, current_user_id: int):
        comment = await self.comment_repository.get(comment_id)
        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment not found",
            )

        if comment.author_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to delete this comment",
            )
        await self.comment_repository.delete(comment)

    async def get_comments_by_task(self, task_id: int, limit: int = 100, page: int = 1):
        offset = (page - 1) * limit
        return await self.comment_repository.get_all_by_field(
            field_name="task_id",
            field_value=task_id,
            limit=limit,
            offset=offset,
        )

    async def get_comments_by_author(
        self, author_id: int, limit: int = 100, page: int = 1
    ):
        offset = (page - 1) * limit
        return await self.comment_repository.get_all_by_field(
            field_name="author_id",
            field_value=author_id,
            limit=limit,
            offset=offset,
        )
