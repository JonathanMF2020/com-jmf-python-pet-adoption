from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class AnimalType(Base):
    __tablename__ = 'animal_type'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(40), index=True)
    filename = Column(String(255), nullable=True)
    path = Column(String(255), nullable=True)
    pets = relationship("Pet", back_populates="animal_type")