from sqlalchemy import Column, ForeignKey, Integer, String
from app.database import Base

class Tag(Base):
    __tablename__ = 'tags'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(40), index=True)
    color = Column(String(40))

class PetTag(Base):
    __tablename__ = 'pet_tags'
    
    pet_id = Column(Integer, ForeignKey('pets.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True)