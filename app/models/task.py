from datetime import datetime, timezone

from sqlalchemy import String,Text,DateTime, ForeignKey,CheckConstraint,Index

# For Join Table
from sqlalchemy.orm import relationship,Mapped, mapped_column

#from database import Base
from app.db.base import Base

# Categories Table
class Task(Base):
    __tablename__ = "tasks"

    __table_args__ = (
        CheckConstraint(
            "priority IN ('low', 'medium', 'high', 'urgent')",
            name="check_task_priority"
        ),
        CheckConstraint(
            "status IN ('todo', 'in_progress', 'review', 'completed')",
            name="check_task_status"
        ),
        Index("ix_tasks_project_status", "project_id", "status"),
        Index("ix_tasks_assigned_status", "assigned_to", "status"),
    )

    id:Mapped[int]                  = mapped_column(primary_key=True)
    project_id:Mapped[int]          = mapped_column(ForeignKey("projects.id",ondelete="CASCADE"), nullable=False, index=True)
    title:Mapped[str]               = mapped_column(String(200), nullable=False)
    description:Mapped[str | None]  = mapped_column(Text, nullable=True)
    assigned_to:Mapped[int | None]  = mapped_column(ForeignKey("users.id",ondelete="SET NULL"), nullable=True, index=True)
    priority:Mapped[str]            = mapped_column(String(20), nullable=False, default="medium")
    status:Mapped[str]              = mapped_column(String(20), nullable=False, default="todo")
    created_by:Mapped[int]          = mapped_column(ForeignKey("users.id",ondelete="RESTRICT"), nullable=True)
    due_date:Mapped[DateTime | None]= mapped_column(DateTime(timezone=True), nullable=True)
    created_at:Mapped[DateTime]     = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at:Mapped[DateTime]     = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    project         = relationship("Project",back_populates="tasks")
    creator         = relationship("User", foreign_keys=[created_by])
    assignee        = relationship("User", back_populates="assigned_tasks", foreign_keys=[assigned_to])
    activity_logs   = relationship("TaskActivity", back_populates="task", cascade="all, delete-orphan")