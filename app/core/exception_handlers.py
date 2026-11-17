from fastapi import Request
from fastapi.responses import JSONResponse
from app.core.exceptions import (
        AppException, EmailAlreadyExistsError,UserNotFoundError,InvalidTokenError,
        ProjectAlreadyExistsError, ProjectNotFoundError, TaskNotFoundError
    )

async def app_exception_handler(
    request: Request,
    exc: AppException,
) -> JSONResponse:
    status_code = 400

    if isinstance(exc, (EmailAlreadyExistsError, ProjectAlreadyExistsError)):
        status_code = 409

    elif isinstance(exc, (UserNotFoundError, ProjectNotFoundError, TaskNotFoundError)):
        status_code = 404

    elif isinstance(exc, InvalidTokenError):
        status_code = 401

    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "message": exc.message,
        },
    )