from sqlalchemy import func, select, extract
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task
#Repositories: Performs database queries : Healper class to interact with the database for budget-related operations.
        
class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, task_id: int, user_id: int) -> Task | None:
        result = await self.db.execute(
            select(Task).where(
                Task.id == task_id,
                Task.assigned_to == user_id,
            )
        )
        return result.scalar_one_or_none()

    async def create(self, task_data: dict) -> Task:
        task = Task(**task_data)
        self.db.add(task)
        await self.db.flush()
        await self.db.refresh(task)
        return task

    async def update(self, task: Task, update_data: dict) -> Task:
        for key, value in update_data.items():
            setattr(task, key, value)
        await self.db.flush()
        await self.db.refresh(task)
        return task

    async def delete(self, task: Task) -> None:
        await self.db.delete(task)
        await self.db.flush()

    async def get_all(self, user_id: int, offset: int, limit: int) -> tuple[list[Task], int]:
        result = await self.db.execute(
            select(Task)
            .where(Task.assigned_to == user_id)
            .order_by(Task.id.desc())
            .offset(offset)
            .limit(limit)
        )

        tasks = list(result.scalars().all())
        count_total = await self.db.execute(
            select(func.count())
            .select_from(Task)
            .where(Task.assigned_to == user_id)
        )
        total = count_total.scalar_one()

        return tasks, total
    
    async def get_project_tasks(self, project_id: int, user_id: int, offset: int, limit: int) -> tuple[list[Task], int]:
        result = await self.db.execute(
            select(Task)
            .where(Task.project_id == project_id, Task.assigned_to == user_id)
            .order_by(Task.id.desc())
            .offset(offset)
            .limit(limit)
        )

        tasks = list(result.scalars().all())
        count_total = await self.db.execute(
            select(func.count())
            .select_from(Task)
            .where(Task.project_id == project_id, Task.assigned_to == user_id)
        )
        total = count_total.scalar_one()

        return tasks, total
        
    