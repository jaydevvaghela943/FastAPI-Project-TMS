from fastapi import FastAPI

from app.api.v1.route import api_router
from app.core.config import settings

# Error Handling
from app.core.exceptions import AppException
from app.core.exception_handlers import app_exception_handler

#from app.lifespan import lifespan

app = FastAPI(title=settings.APP_NAME,version=settings.APP_VERSION,debug=settings.DEBUG,description="Task Management API using FastAPI and PostgreSQL",)

#Exception Handling
app.add_exception_handler(AppException,app_exception_handler)

app.include_router(api_router,prefix="/api/v1")

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy","application": settings.APP_NAME,}