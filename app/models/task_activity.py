from datetime import datetime, timezone

from sqlalchemy import String,ForeignKey,Text,DateTime

# For Join Table
from sqlalchemy.orm import relationship,Mapped, mapped_column

#from database import Base
from app.db.base import Base

# Transactions Table
class TaskActivity(Base):
    __tablename__ = "task_activity_logs"

    id:Mapped[int]              = mapped_column(primary_key=True)
    task_id:Mapped[int]         = mapped_column(ForeignKey("tasks.id",ondelete="CASCADE"), nullable=False, index=True)
    user_id:Mapped[int]         = mapped_column(ForeignKey("users.id",ondelete="RESTRICT"), nullable=False)
    action:Mapped[str]          = mapped_column(String(100), nullable=False)
    old_value:Mapped[str | None]= mapped_column(Text, nullable=True)
    new_value:Mapped[str | None]= mapped_column(Text, nullable=True)
    created_at:Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    # Each Transactions belongs to tables
    task  = relationship("Task", back_populates="activity_logs")
    user = relationship("User", back_populates="activity_logs")