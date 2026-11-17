from math import ceil
from sqlalchemy.ext.asyncio import AsyncSession

# Budget Related Imports
from app.core.exceptions import TaskNotFoundError 
from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskCreate, TaskUpdate

class TaskService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.task_repository = TaskRepository(db)

    async def create_task(self, data: TaskCreate, user_id: int , project_id: int | None = None):
        project_id = project_id if project_id is not None else data.project_id
        task_data = {
            "title": data.title,
            "description": data.description,
            "assigned_to": user_id,
            "status": data.status,
            "project_id": project_id,
            "priority": data.priority,
            "due_date": data.due_date,
        }
        try:
            new_task = await self.task_repository.create(task_data)
            await self.db.commit()
            return new_task
        except Exception:
            await self.db.rollback()
            raise

    async def get_task_by_id(self, task_id: int, user_id: int):
        task = await self.task_repository.get_by_id(task_id, user_id)
        if not task:
            raise TaskNotFoundError(f"Task with ID {task_id} not found.")
        return task

    async def update_task(
        self, task_id: int, data: TaskUpdate, user_id: int
    ):
        task = await self.get_task_by_id(task_id, user_id)
        update_data = data.model_dump(exclude_unset=True, exclude_none=True)

        if not update_data:
            return task
        
        try:
            task = await self.task_repository.update(task, update_data)
            await self.db.commit()
            return task
        except Exception:
            await self.db.rollback()
            raise

    async def delete_task(self, task_id: int, user_id: int):
        task = await self.get_task_by_id(task_id, user_id)
        try:
            await self.task_repository.delete(task)
            await self.db.commit()
        except Exception:
            await self.db.rollback()
            raise

    async def get_tasks(self, user_id: int, page: int = 1, size: int = 10):
        offset = (page - 1) * size
        tasks, total = await self.task_repository.get_all(
            user_id=user_id, offset=offset, limit=size
        )
        total_pages = ceil(total / size) if total > 0 else 1
        return {
            "items": tasks,
            "total": total,
            "page": page,
            "size": size,
            "pages": total_pages,
        }

    async def update_task_status(self, task_id: int, data: TaskUpdate, user_id: int):
        task = await self.get_task_by_id(task_id, user_id)
        update_data = data.model_dump(exclude_unset=True, exclude_none=True)

        if not update_data:
            return task
        
        try:
            task = await self.task_repository.update(task, update_data)
            await self.db.commit()
            return task
        except Exception:
            await self.db.rollback()
            raise

    async def get_project_tasks(self, project_id: int, user_id: int, page: int = 1, size: int = 10):
        offset = (page - 1) * size
        tasks, total = await self.task_repository.get_project_tasks(
            project_id=project_id,
            user_id=user_id,
            offset=offset,
            limit=size
        )

        total_pages = ceil(total / size) if total > 0 else 1
        return {
            "items": tasks,
            "total": total,
            "page": page,
            "size": size,
            "pages": total_pages,
        }