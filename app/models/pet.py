from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.animal_type import AnimalType
from app.models.breed import Breed
from app.models.tag import Tag, PetTag

class Pet(Base):
    __tablename__ = "pets"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    breed_id = Column(Integer,ForeignKey('breed.id'), nullable=False)
    description = Column(Text)
    available = Column(Boolean, default=True)
    filename = Column(String(255), nullable=True)
    path = Column(String(255), nullable=True)
    animal_type_id = Column(Integer, ForeignKey('animal_type.id'), nullable=False)
    tags = relationship('Tag', secondary='pet_tags')
    adoption = relationship("Adoption", back_populates="pet", uselist=False)  # Asegúrate de que esto sea una relación uno a uno
    animal_type = relationship("AnimalType", back_populates="pets")
    breed = relationship("Breed", back_populates="pets")