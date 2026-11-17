from fastapi import APIRouter

from app.api.v1.endpoints import auth, users,projects,tasks,task_activity_logs


api_router = APIRouter()

api_router.include_router(users.router)
api_router.include_router(auth.router)
api_router.include_router(projects.router)
api_router.include_router(tasks.router)
