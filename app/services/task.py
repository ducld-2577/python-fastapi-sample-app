from fastapi import HTTPException
from starlette import status

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
    ):
        self.task_repository = task_repository
        self.project_repository = project_repository
        self.user_repository = user_repository

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

    async def get_tasks_by_project(self, project_id):
        project = await self.project_repository.get(project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )
        # TODO: pagination and cache
        return await self.task_repository.get_tasks_by_project(project_id)

    async def get_tasks_by_assignee(self, assignee_id):
        user = await self.user_repository.get(assignee_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        # TODO: pagination and cache
        return await self.task_repository.get_tasks_by_assignee(assignee_id)

    async def update_task_status(self, task_id, TaskUpdateStatus):
        task = await self.task_repository.get(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )
        await self.task_repository.update_task_status(task_id, TaskUpdateStatus.status)

        return {
            "message": f"Task {task_id} status updated to {TaskUpdateStatus.status}"
        }

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

        return {
            "message": f"Task {task_id} priority updated to {TaskUpdatePriority.priority}"
        }

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

        return {"message": f"Task {task_id} assigned to user {TaskAssign.assignee_id}"}

    async def get_task(self, task_id):
        task = await self.task_repository.get(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )
        return task

    async def delete_task(self, task_id):
        task = await self.task_repository.get(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )
        await self.task_repository.delete(task)
        return {"message": f"Task {task_id} deleted successfully"}

    async def update_task(self, task_id, payload: TaskUpdate):
        task = await self.task_repository.get(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )
        task.title = payload.title
        task.description = payload.description
        return await self.task_repository.update(task)
