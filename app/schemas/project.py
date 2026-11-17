from datetime import datetime,date
from pydantic import BaseModel, ConfigDict, Field

# Create project
class ProjectCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=150
    )

    description: str | None = None
    status: str | None = Field(
        default="active",
        pattern="^(active|completed|archived)$"
    )
    start_date: date | None = None
    end_date: date | None = None


# Update project
class ProjectUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=150
    )

    description: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    

    model_config = ConfigDict(extra="forbid")


# Project response
class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str | None
    owner_id: int
    status: str
    start_date: date | None
    end_date: date | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Project list response
class ProjectList(BaseModel):
    items: list[ProjectResponse]
    total: int
    page: int
    size: int
    pages: int

    model_config = ConfigDict(from_attributes=True) 