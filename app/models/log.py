from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from app.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class Log(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True, index=True)
    service = Column(String(100))
    type = Column(String(30))
    description = Column(Text)
    timestamp = Column(DateTime(timezone=True), default=func.now())
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="logs")

