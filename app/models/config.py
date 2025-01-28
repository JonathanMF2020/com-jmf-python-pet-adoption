from sqlalchemy import Column, Integer, Text
from app.database import Base

class Config(Base):
    __tablename__ = "configs"
    id = Column(Integer, primary_key=True, index=True)
    key = Column(Text, nullable=False)
    value = Column(Text, nullable=False)