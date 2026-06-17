from app.models.label import Label, task_labels
from app.repositories.base import BaseRepository
from sqlalchemy import select, insert, delete


class LabelRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(Label, session)

    async def get_all(
        self,
        limit: int = 10,
        offset: int = 0,
    ):
        result = await self.session.execute(
            select(Label).order_by(Label.id.desc()).limit(limit).offset(offset)
        )
        return result.scalars().all()

    async def get_labels_by_project(
        self,
        project_id: int,
        limit: int = 10,
        offset: int = 0,
    ):
        result = await self.session.execute(
            select(Label)
            .where(Label.project_id == project_id)
            .order_by(Label.id.desc())
            .limit(limit)
            .offset(offset)
        )
        return result.scalars().all()

    async def get_labels_by_task_id(self, task_id: int):
        result = await self.session.execute(
            select(Label)
            .join(task_labels, task_labels.c.label_id == Label.id)
            .where(task_labels.c.task_id == task_id)
            .order_by(Label.id.desc())
        )
        return result.scalars().all()

    async def assign_label_to_task(self, task_id: int, label_id: int):
        stmt = insert(task_labels).values(
            task_id=task_id,
            label_id=label_id,
        )
        await self.session.execute(stmt)
        await self.session.commit()

    async def remove_label_from_task(self, task_id: int, label_id: int):
        stmt = delete(task_labels).where(
            task_labels.c.task_id == task_id,
            task_labels.c.label_id == label_id,
        )
        await self.session.execute(stmt)
        await self.session.commit()
