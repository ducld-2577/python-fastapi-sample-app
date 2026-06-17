from fastapi import HTTPException
from starlette import status

from app.models.label import Label
from app.repositories.label import LabelRepository
from app.repositories.project import ProjectRepository
from app.repositories.task import TaskRepository
from app.schemas.label import LabelAssignTask, LabelCreate, LabelUpdate


class LabelService:
    def __init__(
        self,
        label_repository: LabelRepository,
        task_repository: TaskRepository,
        project_repository: ProjectRepository,
    ):
        self.label_repository = label_repository
        self.task_repository = task_repository
        self.project_repository = project_repository

    async def get_labels(self, limit: int = 100, page: int = 1):
        offset = (page - 1) * limit
        return await self.label_repository.get_all(limit=limit, offset=offset)

    async def create_label(self, payload: LabelCreate):
        project = await self.project_repository.get(payload.project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found",
            )

        label = Label(
            project_id=payload.project_id,
            name=payload.name,
            color=payload.color,
        )
        return await self.label_repository.create(label)

    async def update_label(self, label_id: int, payload: LabelUpdate):
        label = await self.label_repository.get(label_id)
        if not label:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Label not found",
            )

        if payload.name is not None:
            label.name = payload.name
        if payload.color is not None:
            label.color = payload.color

        return await self.label_repository.update(label)

    async def delete_label(self, label_id: int):
        label = await self.label_repository.get(label_id)
        if not label:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Label not found",
            )
        await self.label_repository.delete(label)

    async def assign_label_to_task(self, payload: LabelAssignTask):
        task = await self.task_repository.get(payload.task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )
        label = await self.label_repository.get(payload.label_id)
        if not label:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Label not found",
            )
        await self.label_repository.assign_label_to_task(
            payload.task_id, payload.label_id
        )

    async def get_labels_by_task_id(self, task_id: int):
        task = await self.task_repository.get(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )
        return await self.label_repository.get_labels_by_task_id(task_id)

    async def get_labels_by_project(
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
        return await self.label_repository.get_labels_by_project(
            project_id=project_id,
            limit=page_size,
            offset=offset,
        )

    async def remove_label_from_task(self, payload: LabelAssignTask):
        task = await self.task_repository.get(payload.task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found",
            )
        label = await self.label_repository.get(payload.label_id)
        if not label:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Label not found",
            )
        await self.label_repository.remove_label_from_task(
            payload.task_id, payload.label_id
        )
