from sqlalchemy import select
from app.models.comment import Comment
from app.repositories.base import BaseRepository


class CommentRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(Comment, session)

    async def get_all_by_field(
        self,
        field_name: str,
        field_value,
        limit: int = 10,
        offset: int = 0,
    ):
        query = (
            select(self.model)
            .filter(getattr(self.model, field_name) == field_value)
            .order_by(self.model.id.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return result.scalars().all()
