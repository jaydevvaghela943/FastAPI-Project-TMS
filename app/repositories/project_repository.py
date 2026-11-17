from sqlalchemy import func, select, extract
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project
#Repositories: Performs database queries : Healper class to interact with the database for budget-related operations.

class ProjectRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, project_id: int, user_id: int) -> Project | None:
        result = await self.db.execute(
            select(Project).where(
                Project.id == project_id,
                Project.owner_id == user_id,
            )
        )
        return result.scalar_one_or_none()

    async def create(self, project_data: dict) -> Project:
        project = Project(**project_data)
        self.db.add(project)
        await self.db.flush()
        await self.db.refresh(project)
        return project

    async def update(self, project: Project, update_data: dict) -> Project:
        for key, value in update_data.items():
            setattr(project, key, value)
        await self.db.flush()
        await self.db.refresh(project)
        return project

    async def delete(self, project: Project) -> None:
        await self.db.delete(project)
        await self.db.flush()

    async def get_all(
        self, user_id: int, offset: int, limit: int
    ) -> tuple[list[Project], int]:
        result = await self.db.execute(
            select(Project)
            .where(Project.owner_id == user_id)
            .order_by(Project.id.desc())
            .offset(offset)
            .limit(limit)
        )

        budgets = list(result.scalars().all())
        count_total = await self.db.execute(
            select(func.count())
            .select_from(Project)
            .where(Project.owner_id == user_id)
        )
        total = count_total.scalar_one()

        return budgets, total