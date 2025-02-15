from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(100))
    is_admin = Column(Boolean, default=False)
    tags = relationship('Tag', secondary='users_tag')
    permissions = relationship("Permission", secondary="profiles_permissions", back_populates="users")
    logs = relationship("Log", back_populates="user")

class UserTag(Base):
    __tablename__ = 'users_tag'
    
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True) 
    tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True)
    