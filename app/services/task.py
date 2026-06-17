import json
from fastapi import HTTPException
from starlette import status
from redis.asyncio import Redis

from app.models.task import Task
from app.repositories.project import ProjectRepository
from app.repositories.task import TaskRepository
from app.repositories.user import UserRepository
from app.schemas.task import TaskCreate, TaskUpdate


class TaskService:
    def __init__(
        self,
        task_repository: TaskRepository,
        user_repository: UserRepository,
        project_repository: ProjectRepository,
        redis_client: Redis,
        settings,
    ):
        self.task_repository = task_repository
        self.project_repository = project_repository
        self.user_repository = user_repository
        self.redis_client = redis_client
        self.settings = settings

    def _get_task_cache_key(self, task_id: int) -> str:
        """Generate cache key for a task"""
        return f"task:{task_id}"

    async def _save_task_to_cache(self, task_id: int, task) -> None:
        """Save task to cache with TTL from settings"""
        cache_key = self._get_task_cache_key(task_id)
        task_dict = {
            "id": task.id,
            "project_id": task.project_id,
            "assignee_id": task.assignee_id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "priority": task.priority,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "created_at": (
                task.created_at.isoformat()
                if hasattr(task, "created_at") and task.created_at
                else None
            ),
            "updated_at": (
                task.updated_at.isoformat()
                if hasattr(task, "updated_at") and task.updated_at
                else None
            ),
        }
        await self.redis_client.setex(
            cache_key,
            self.settings.task_cache_ttl,
            json.dumps(task_dict),
        )

    async def _invalidate_task_cache(self, task_id: int) -> None:
        """Invalidate cache for a specific task"""
        cache_key = self._get_task_cache_key(task_id)
        await self.redis_client.delete(cache_key)

    async def create_task(self, payload: TaskCreate):
        project = await self.project_repository.get(payload.project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )

        if payload.assignee_id:
            assignee = await self.user_repository.get(payload.assignee_id)
            if not assignee:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Assignee not found",
                )

        task = Task(
            project_id=payload.project_id,
            assignee_id=payload.assignee_id,
            title=payload.title,
            description=payload.description,
            status=payload.status,
            priority=payload.priority,
            due_date=payload.due_date,
        )
        return await self.task_repository.create(task)

    async def get_tasks_by_project(
        self,
        project_id: int,
        page: int = 1,
        page_size: int = 10,
    ):
        project = await self.project_repository.get(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )

        offset = (page - 1) * page_size
        return await self.task_repository.get_tasks_by_project(
            project_id=project_id,
            limit=page_size,
            offset=offset,
        )

    async def get_tasks_by_assignee(
        self,
        assignee_id: int,
        page: int = 1,
        page_size: int = 10,
    ):
        user = await self.user_repository.get(assignee_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        offset = (page - 1) * page_size
        return await self.task_repository.get_tasks_by_assignee(
            assignee_id=assignee_id,
            limit=page_size,
            offset=offset,
        )

    async def update_task_status(self, task_id, TaskUpdateStatus):
        task = await self.task_repository.get(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )
        await self.task_repository.update_task_status(task_id, TaskUpdateStatus.status)

        # Invalidate cache
        await self._invalidate_task_cache(task_id)

        return await self.task_repository.get(task_id)

    async def update_task_priority(self, task_id, TaskUpdatePriority):
        task = await self.task_repository.get(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )
        await self.task_repository.update_task_priority(
            task_id, TaskUpdatePriority.priority
        )

        # Invalidate cache
        await self._invalidate_task_cache(task_id)

        return await self.task_repository.get(task_id)

    async def assign_task(self, task_id, TaskAssign):
        task = await self.task_repository.get(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        user = await self.user_repository.get(TaskAssign.assignee_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        await self.task_repository.assign_task(task_id, TaskAssign.assignee_id)

        # Invalidate cache
        await self._invalidate_task_cache(task_id)

        return await self.task_repository.get(task_id)

    async def get_task(self, task_id):
        cache_key = self._get_task_cache_key(task_id)

        cached_task = await self.redis_client.get(cache_key)
        if cached_task:
            return json.loads(cached_task)

        task = await self.task_repository.get(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )

        await self._save_task_to_cache(task_id, task)
        return task

    async def delete_task(self, task_id):
        task = await self.task_repository.get(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )
        await self.task_repository.delete(task)

        # Invalidate cache
        await self._invalidate_task_cache(task_id)

        return await self.task_repository.get(task_id)

    async def update_task(self, task_id, payload: TaskUpdate):
        task = await self.task_repository.get(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )
        task.title = payload.title
        task.description = payload.description
        await self.task_repository.update(task)

        # Invalidate cache
        await self._invalidate_task_cache(task_id)

        return await self.task_repository.get(task_id)
