from app.repositories.base import BaseRepository
from app.models.user import User
from sqlalchemy import select


class UserRepository(BaseRepository[User]):
    def __init__(self, session):
        super().__init__(User, session)

    async def get_by_email(self, email: str):
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create_user(self, email: str, full_name: str, hashed_password: str):
        new_user = User(
            email=email,
            full_name=full_name,
            hashed_password=hashed_password,
        )
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return new_user
