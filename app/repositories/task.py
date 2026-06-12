from app.repositories.base import BaseRepository
from app.models.task import Task, TaskStatus, TaskPriority


class TaskRepository(BaseRepository):
    def __init__(self, session):
        from app.models.task import Task

        super().__init__(Task, session)

    async def get_tasks_by_project(self, project_id: int):
        from sqlalchemy import select

        result = await self.session.execute(
            select(Task).where(Task.project_id == project_id)
        )
        return result.scalars().all()

    async def update_task_status(self, task_id: int, new_status: TaskStatus):
        from sqlalchemy import update

        await self.session.execute(
            update(Task).where(Task.id == task_id).values(status=new_status)
        )
        await self.session.commit()

    async def update_task_priority(self, task_id: int, new_priority: TaskPriority):
        from sqlalchemy import update

        await self.session.execute(
            update(Task).where(Task.id == task_id).values(priority=new_priority)
        )
        await self.session.commit()

    async def get_tasks_by_assignee(self, assignee_id: int):
        from sqlalchemy import select

        result = await self.session.execute(
            select(Task).where(Task.assignee_id == assignee_id)
        )
        return result.scalars().all()

    async def assign_task(self, task_id: int, assignee_id: int):
        from sqlalchemy import update

        await self.session.execute(
            update(Task).where(Task.id == task_id).values(assignee_id=assignee_id)
        )
        await self.session.commit()
