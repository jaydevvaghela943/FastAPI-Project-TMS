from math import ceil
from sqlalchemy.ext.asyncio import AsyncSession

# Budget Related Imports
from app.core.exceptions import ProjectNotFoundError 
from app.repositories.project_repository import ProjectRepository
from app.schemas.project import ProjectCreate, ProjectUpdate

class ProjectService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.project_repository = ProjectRepository(db)

    async def create_project(self, data: ProjectCreate, user_id: int):
        project_data = {
            "name": data.name,
            "description": data.description,
            "owner_id": user_id,
            "status": data.status,
            "start_date": data.start_date,
            "end_date": data.end_date
        }
        try:
            new_project = await self.project_repository.create(project_data)
            await self.db.commit()
            return new_project
        except Exception:
            await self.db.rollback()
            raise
    
    async def get_project_by_id(self, project_id: int, user_id: int):
        project = await self.project_repository.get_by_id(project_id, user_id)
        if not project:
            raise ProjectNotFoundError(f"Project with ID {project_id} not found.")
        return project

    async def update_project(
        self, project_id: int, data: ProjectUpdate, user_id: int
    ):
        project = await self.get_project_by_id(project_id, user_id)
        update_data = data.model_dump(exclude_unset=True, exclude_none=True)

        if not update_data:
            return project
        
        try:
            project = await self.project_repository.update(project, update_data)
            await self.db.commit()
            return project
        except Exception:
            await self.db.rollback()
            raise

    async def delete_project(self, project_id: int, user_id: int):
        project = await self.get_project_by_id(project_id, user_id)
        try:
            await self.project_repository.delete(project)
            await self.db.commit()
        except Exception:
            await self.db.rollback()
            raise

    async def get_projects(self, user_id: int, page: int = 1, size: int = 10):
        offset = (page - 1) * size
        projects, total = await self.project_repository.get_all(
            user_id=user_id, offset=offset, limit=size
        )
        total_pages = ceil(total / size) if total > 0 else 1
        return {
            "items": projects,
            "total": total,
            "page": page,
            "size": size,
            "pages": total_pages,
        }