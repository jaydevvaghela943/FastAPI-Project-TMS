from typing import Annotated
from fastapi import Depends, Response, status,APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependency import get_current_user
from app.db.dependencies import get_db
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate
from app.services.user_service import UserService


router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserResponse)
async def get_my_profile(current_user: Annotated[User, Depends(get_current_user)]):
    """
    Get the profile of the currently authenticated user.
    """
    return current_user

@router.patch("/me", response_model=UserResponse)
async def update_my_profile(
    data: UserUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]):
    """
    Update the profile of the currently authenticated user.
    """
    user_service = UserService(db)
    return await user_service.update_user(user_id=current_user.id, data=data)

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_my_profile(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]):
    """
    Delete the profile of the currently authenticated user.
    """
    user_service = UserService(db)
    await user_service.delete_user(user_id=current_user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)