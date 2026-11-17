from typing import Annotated
from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependency import get_current_user
from app.db.dependencies import get_db
from app.models.user import User
from app.schemas.project import ProjectCreate,ProjectResponse,ProjectUpdate,ProjectList
from app.schemas.task import TaskCreate, ProjectTaskCreate, TaskList, TaskResponse
from app.services.project_service import ProjectService
from app.services.task_service import TaskService


router = APIRouter(prefix="/projects", tags=["Projects"])

# Annotated: 
# In FastAPI, Annotated is used to attach additional information (metadata) to a Python type without changing the type itself.
# Benefit:Less repeated code, cleaner endpoints, and easier maintenance.: define one time and use multiple times.

#Annotated Example: ge=1 : Means greater than or equal to 1
CurrentUser= Annotated[User, Depends(get_current_user)] # CurrentUser: User = Depends(get_current_user)
page_param = Annotated[int,Query(ge=1, description="Page number for pagination")]
size_param = Annotated[int,Query(ge=1, description="Number of items per page")]
db_session = Annotated[AsyncSession, Depends(get_db)]


@router.get("/", response_model=ProjectList)
async def get_projects(current_user: CurrentUser,db: db_session,page: page_param = 1,size: size_param = 10):
    project_service = ProjectService(db)
    return await project_service.get_projects(user_id=current_user.id,page=page,size=size)


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(data: ProjectCreate,current_user: CurrentUser,db: db_session):
    project_service = ProjectService(db)
    return await project_service.create_project(data=data, user_id=current_user.id)


@router.patch("/{project_id}", response_model=ProjectResponse)
async def update_project(project_id: int,data: ProjectUpdate,current_user: CurrentUser,db: db_session):
    project_service = ProjectService(db)
    return await project_service.update_project(project_id=project_id,data=data,user_id=current_user.id)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: int,current_user: CurrentUser,db: db_session):
    project_service = ProjectService(db)
    await project_service.delete_project(project_id=project_id,user_id=current_user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.post("/{project_id}/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(project_id: int,data: ProjectTaskCreate,current_user: CurrentUser,db: db_session):
    task_service = TaskService(db)
    return await task_service.create_task(data=data, user_id=current_user.id, project_id=project_id)

@router.get("/{project_id}/tasks", response_model=TaskList)
async def get_tasks(project_id: int,current_user: CurrentUser,db: db_session,page: page_param = 1,size: size_param = 10):
    task_service = TaskService(db)
    return await task_service.get_project_tasks(project_id=project_id,user_id=current_user.id,page=page,size=size)