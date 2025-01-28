from pydantic import BaseModel
from typing import Optional, List

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
        orm_mode = True

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
        orm_mode = True

class PetCreate(BaseModel):
    name: str
    age: int
    breed_id: int
    animal_type_id: int
    description: Optional[str] = None
    available: bool = True
    
class PetBase(BaseModel):
    id: int
    name: str
    age: int
    breed_id: int
    animal_type_id: int
    description: Optional[str] = None
    available: bool = True
    tags: List[TagSchema]
    adoption_evaluation: Optional[AdoptionEvaluationBase] = None 
    
    class Config:
        orm_mode = True

        
