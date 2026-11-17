from sqlalchemy.ext.asyncio import AsyncSession

#JWT related
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from app.core.config import settings
from app.models.user import User
from app.db.dependencies import get_db
from app.repositories.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

#Annotated:
# In FastAPI, Annotated is used to attach additional information (metadata) to a Python
# Simple Share variable: define one time and use multiple times.

token_param = Annotated[str, Depends(oauth2_scheme)]
db_session = Annotated[AsyncSession, Depends(get_db)]

async def get_current_user(token: token_param, db: db_session) -> User:
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials",headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id = int(payload["sub"])
    except (JWTError, KeyError, TypeError, ValueError):
        raise credentials_exception

    user_repo = UserRepository(db)
    user = await user_repo.get_by_id(user_id)
    if user is None:
        raise credentials_exception
    return user
