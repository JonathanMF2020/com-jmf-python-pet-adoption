from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Breed(Base):
    __tablename__ = 'breed'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(40), index=True)
    pets = relationship("Pet", back_populates="breed")