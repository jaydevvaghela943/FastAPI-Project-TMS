from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.dependencies import get_db
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.schemas.auth import RefreshTokenRequest, TokenResponse, UserRegister, UserResponse
from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    repository = UserRepository(db)
    service = AuthService(repository, db)
    user = await service.authenticate_user(form_data.username, form_data.password)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    refresh_token = await service.issue_refresh_token(user.id)
    return TokenResponse(
        access_token=create_access_token(user.id),
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=3600  # Token expiration time in seconds""
    )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    payload: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db),
):
    repository = UserRepository(db)
    service = AuthService(repository, db)
    await service.revoke_refresh_token(payload.refresh_token)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
async def register_user(
    payload: UserRegister,
    db: AsyncSession = Depends(get_db)
):
    repository = UserRepository(db)
    service = AuthService(repository, db)

    return await service.register_user(payload)