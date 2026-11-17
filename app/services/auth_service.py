from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from jose import JWTError, jwt
from sqlalchemy import select

from app.repositories.user_repository import UserRepository
from app.core.config import settings
from app.core.exceptions import InvalidTokenError
from app.core.security import (
    create_refresh_token,
    hash_password,
    hash_token,
    verify_password,
)

from app.schemas.auth import UserRegister
from app.models.refresh_token import RefreshToken
from app.models.user import User


class AuthService:
    def __init__(self, user_repository: UserRepository, db):
        self.user_repository = user_repository
        self.db = db

    async def authenticate_user(self, email: str, password: str) -> User | None:
        user = await self.user_repository.get_by_email(email.strip().lower())

        if user is None or not verify_password(password, user.password_hash):
            return None

        return user

    async def register_user(self, payload: UserRegister):
        email = str(payload.email).strip().lower()
        existing_user = await self.user_repository.get_by_email(email)

        if existing_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")

        user_data = {
            "name": payload.name.strip(),
            "email": email,
            "password_hash": hash_password(payload.password)
        }

        try:
            user = await self.user_repository.create(user_data)
            await self.db.commit()
            return user
        except Exception:
            await self.db.rollback()
            raise

    async def issue_refresh_token(self, user_id: int) -> str:
        expires_at = datetime.now(timezone.utc) + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )
        token = create_refresh_token(user_id, expires_at)
        self.db.add(
            RefreshToken(
                token_hash=hash_token(token),
                expires_at=expires_at,
                revoked_at=None,
                user_id=user_id,
            )
        )
        try:
            await self.db.commit()
        except Exception:
            await self.db.rollback()
            raise
        return token

    async def revoke_refresh_token(self, token: str) -> None:
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )
            if payload.get("type") != "refresh":
                raise InvalidTokenError("Invalid refresh token")
            user_id = int(payload["sub"])
        except (JWTError, KeyError, TypeError, ValueError):
            raise InvalidTokenError("Invalid refresh token") from None

        result = await self.db.execute(
            select(RefreshToken).where(RefreshToken.token_hash == hash_token(token))
        )
        refresh_token = result.scalar_one_or_none()
        now = datetime.now(timezone.utc)
        if (
            refresh_token is None
            or refresh_token.user_id != user_id
            or refresh_token.revoked_at is not None
        ):
            raise InvalidTokenError("Invalid refresh token")

        expires_at = refresh_token.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        if expires_at <= now:
            raise InvalidTokenError("Invalid refresh token")

        refresh_token.revoked_at = now
        try:
            await self.db.commit()
        except Exception:
            await self.db.rollback()
            raise