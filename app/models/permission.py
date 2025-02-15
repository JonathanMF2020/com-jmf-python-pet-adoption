from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String, Text
from app.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class Permission(Base):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    available = Column(Boolean, default=True)
    users = relationship("User", secondary="profiles_permissions", back_populates="permissions")

    
class ProfilePermissions(Base):
    __tablename__ = "profiles_permissions"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(Date, default=func.now())
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    permision_id = Column(Integer, ForeignKey("permissions.id", ondelete="CASCADE"), nullable=False)

