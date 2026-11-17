from sqlalchemy import Boolean, CheckConstraint,String,DateTime
from datetime import datetime, timezone

# For 
from sqlalchemy.orm import relationship,Mapped, mapped_column

#from database import Base
from app.db.base import Base

# User Table
class User(Base):
    __tablename__ = "users"

    __table_args__ = (
        CheckConstraint(
            "role IN ('admin', 'user')",
            name="check_user_role"
        ),
    )


    id:Mapped[int]              =  mapped_column(primary_key=True,index=True)
    name:Mapped[str]            = mapped_column(String(50),nullable=False)
    email:Mapped[str]           = mapped_column(String(255),unique=True,index=True,nullable=False)
    password_hash:Mapped[str]   = mapped_column(String(255),nullable=False)
    role:Mapped[str]            = mapped_column(String(50),nullable=False,default="user")
    is_active:Mapped[bool]      = mapped_column(Boolean,default=True,nullable=False)
    is_deleted:Mapped[bool]     = mapped_column(Boolean,default=False,nullable=False)
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True),default=lambda: datetime.now(timezone.utc),nullable=False)

    # Relationships : 1-1 or 1-M relationships with other tables
    owned_projects = relationship("Project",back_populates="owner")
    refresh_tokens = relationship("RefreshToken",back_populates="user", cascade="all, delete-orphan")
    assigned_tasks = relationship("Task", back_populates="assignee", foreign_keys="Task.assigned_to")
    activity_logs  = relationship("TaskActivity", back_populates="user")