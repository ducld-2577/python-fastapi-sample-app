from app.repositories.base import BaseRepository
from app.models.task import Task, TaskStatus, TaskPriority
from sqlalchemy import select, update


class TaskRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(Task, session)

    async def get_tasks_by_project(
        self,
        project_id: int,
        limit: int = 10,
        offset: int = 0,
    ):
        result = await self.session.execute(
            select(Task)
            .where(Task.project_id == project_id)
            .order_by(Task.id.desc())
            .limit(limit)
            .offset(offset)
        )
        return result.scalars().all()

    async def update_task_status(self, task_id: int, new_status: TaskStatus):
        await self.session.execute(
            update(Task).where(Task.id == task_id).values(status=new_status)
        )
        await self.session.commit()

    async def update_task_priority(self, task_id: int, new_priority: TaskPriority):
        await self.session.execute(
            update(Task).where(Task.id == task_id).values(priority=new_priority)
        )
        await self.session.commit()

    async def get_tasks_by_assignee(
        self,
        assignee_id: int,
        limit: int = 10,
        offset: int = 0,
    ):
        result = await self.session.execute(
            select(Task)
            .where(Task.assignee_id == assignee_id)
            .order_by(Task.id.desc())
            .limit(limit)
            .offset(offset)
        )
        return result.scalars().all()

    async def assign_task(self, task_id: int, assignee_id: int):
        await self.session.execute(
            update(Task).where(Task.id == task_id).values(assignee_id=assignee_id)
        )
        await self.session.commit()
