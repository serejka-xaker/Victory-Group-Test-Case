from sqlalchemy import String, Integer, Index, DateTime
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base

class URLModel(Base):
    __tablename__ = "urls"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    full_url: Mapped[str] = mapped_column(String, nullable=False)
    
    short_id: Mapped[str] = mapped_column(
        String, 
        unique=True, 
        index=True, 
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc)
    )
    
    clicks: Mapped[int] = mapped_column(Integer, default=0)
