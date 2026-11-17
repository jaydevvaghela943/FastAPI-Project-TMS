from sqlalchemy import select,func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self,user_id:int) -> User | None:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
    
    async def get_by_email(self,email:str) -> User | None:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create(self,user_data:dict) -> User:
        user = User(**user_data)
        self.db.add(user)
        await self.db.flush()
        await self.db.refresh(user)
        return user

    async def update(self,user:User,update_data:dict) -> User:
        for key, value in update_data.items():
            setattr(user, key, value)
        await self.db.flush()
        await self.db.refresh(user)
        return user

    async def delete(self,user:User) -> None:
        await self.db.delete(user)
        await self.db.flush()

    async def get_all(self, offset: int, limit: int) -> tuple[list[User], int]:
        result = await self.db.execute(
            select(User).order_by(User.id.desc()).offset(offset).limit(limit)
        )

        users = list(result.scalars().all())
        count_total = await self.db.execute(select(func.count()).select_from(User))
        total = count_total.scalar_one()

        return users, total