from pydantic import BaseModel
from typing import Optional, List

from app.models.pet import AnimalType, Breed

class TagSchema(BaseModel):
    id: int
    name: str
    
class PetWithTags(BaseModel):
    id: int
    name: str
    age: int  # Agregamos el campo 'age'
    breed: str  # Agregamos el campo 'breed'
    tags: List[TagSchema]  # Lista de etiquetas asociadas al perrito

    class Config:
        from_attributes = True

class AdoptionEvaluationBase(BaseModel):
    behavior: str
    energy_level: str
    good_with_children: bool
    good_with_other_pets: bool
    special_needs: Optional[str] = None
    temperament: str
    
    
class AdoptionEvaluationResponse(AdoptionEvaluationBase):
    id: int
    pet_id: int

    class Config:
        from_attributes = True

class PetCreate(BaseModel):
    name: str
    age: int
    breed_id: int
    animal_type_id: int
    description: Optional[str] = None
    available: bool = True
    
class AnimalTypeBase(BaseModel):
    id: int
    name: str
    
class BreedBase(BaseModel):
    id: int
    name: str
    
class PetBase(BaseModel):
    id: int
    name: str
    age: int
    breed_id: int
    animal_type_id: int
    description: Optional[str] = None
    filename: Optional[str] = None
    path: Optional[str] = None
    available: bool = True
    tags: List[TagSchema]
    animal_type: Optional[AnimalTypeBase] = None 
    breed: Optional[BreedBase] = None 
    adoption_evaluation: Optional[AdoptionEvaluationBase] = None 
    
    class Config:
        from_attributes = True

        
