from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field

class UserCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: EmailStr
    role: Literal["admin", "user"]
    is_active: bool
    is_deleted: bool
    created_at: datetime

class UserUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    email: EmailStr | None = None

    model_config = ConfigDict(extra="forbid")