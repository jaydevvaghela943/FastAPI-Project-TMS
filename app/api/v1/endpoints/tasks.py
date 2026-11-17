from typing import Annotated
from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependency import get_current_user
from app.db.dependencies import get_db
from app.models.user import User
from app.schemas.project import ProjectList
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskList,TaskStatusUpdate
from app.services.project_service import ProjectService
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["Tasks"])

# Annotated: 
# In FastAPI, Annotated is used to attach additional information (metadata) to a Python type without changing the type itself.
# Benefit:Less repeated code, cleaner endpoints, and easier maintenance.: define one time and use multiple times.

#Annotated Example: ge=1 : Means greater than or equal to 1
CurrentUser= Annotated[User, Depends(get_current_user)] # CurrentUser: User = Depends(get_current_user)
page_param = Annotated[int,Query(ge=1, description="Page number for pagination")]
size_param = Annotated[int,Query(ge=1, description="Number of items per page")]
db_session = Annotated[AsyncSession, Depends(get_db)]


@router.get("/", response_model=TaskList)
async def get_tasks(current_user: CurrentUser,db: db_session,page: page_param = 1,size: size_param = 10):
    task_service = TaskService(db)
    return await task_service.get_tasks(user_id=current_user.id,page=page,size=size)


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(data: TaskCreate,current_user: CurrentUser,db: db_session):
    task_service = TaskService(db)
    return await task_service.create_task(data=data, user_id=current_user.id)


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(task_id: int,data: TaskUpdate,current_user: CurrentUser,db: db_session):
    task_service = TaskService(db)
    return await task_service.update_task(task_id=task_id,data=data,user_id=current_user.id)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int,current_user: CurrentUser,db: db_session):
    task_service = TaskService(db)
    await task_service.delete_task(task_id=task_id,user_id=current_user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.patch("/{task_id}/status", response_model=TaskResponse)
async def update_task_status(task_id: int,data: TaskStatusUpdate,current_user: CurrentUser,db: db_session):
    task_service = TaskService(db)
    return await task_service.update_task_status(task_id=task_id,data=data,user_id=current_user.id)
