from datetime import datetime, timezone

from sqlalchemy import String,ForeignKey,DateTime

# For Join Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

#from database import Base
from app.db.base import Base


# Create all table for Database
#=========================================================

#Refresh_tokens Table
class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    
    id:Mapped[int]                      = mapped_column(primary_key=True, index=True)
    token_hash:Mapped[str]              = mapped_column(String(255), unique=True, nullable=False)
    expires_at:Mapped[datetime | None]  = mapped_column(DateTime(timezone=True), nullable=False)
    revoked_at:Mapped[datetime | None]  = mapped_column(DateTime(timezone=True), nullable=True)
    user_id:Mapped[int]                 = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    created_at:Mapped[datetime]         = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    
    # Each Transactions belongs to tables
    user = relationship("User", back_populates="refresh_tokens")
    
