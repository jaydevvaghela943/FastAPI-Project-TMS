from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


# Create activity
class TaskActivityCreate(BaseModel):
    task_id: int
    action: str = Field(min_length=2,max_length=100)

# Activity response
class TaskActivityResponse(BaseModel):
    id: int
    task_id: int
    user_id: int
    action: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)