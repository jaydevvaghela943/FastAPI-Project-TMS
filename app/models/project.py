from datetime import date,datetime, timezone

from sqlalchemy import ForeignKey,String,Text,Date,DateTime,CheckConstraint

# For Join Table
from sqlalchemy.orm import relationship,Mapped, mapped_column

#from database import Base
from app.db.base import Base

# Budgets Table
class Project(Base):
    __tablename__ = "projects"

    # Check Constraint for Unique or Condition based
    __table_args__ = (
        CheckConstraint(
            "status IN ('active', 'completed', 'archived')",
            name="check_project_status"
        ),
    )


    id:Mapped[int]                  = mapped_column(primary_key=True, index=True)
    name:Mapped[str]                = mapped_column(String(150), nullable=False)
    description:Mapped[str | None]  = mapped_column(Text, nullable=True)
    owner_id:Mapped[int]            = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), index=True, nullable=False)
    status:Mapped[str]              = mapped_column(String(20),  default="active",nullable=False)
    start_date:Mapped[date | None]  = mapped_column(Date, nullable=True)
    end_date:Mapped[date | None]    = mapped_column(Date, nullable=True)
    created_at:Mapped[datetime]     = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    # Each Transactions belongs to tables
    owner = relationship("User", back_populates="owned_projects",foreign_keys=[owner_id])
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")