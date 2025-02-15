from pydantic import BaseModel
from typing import List, Optional
from app.schemas.pet import PetBase
from datetime import datetime

class AdoptionBase(BaseModel):
    pet_id: int
    pet: PetBase
    user_id: int
    latitude: float
    longitude: float
    description: str
    
class ReactionsGet(BaseModel):
    name: str
    
class ReactionResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
    
class AdoptionCommentBaseSchema(BaseModel):
    id: int
    comment: str 
    datetime: datetime
    reactions: List[ReactionResponse]  
    
    class Config:
        from_attributes = True


class AdoptionGet(BaseModel):
    pet: PetBase
    comments: List[AdoptionCommentBaseSchema]
    user_id: int
    latitude: float
    longitude: float
    description: str
    
    class Config:
        from_attributes = True
        
    
class AdoptationEnd(BaseModel):
    pet_id: int
    adopter_id: int
    
class ReactionInComment(BaseModel):
    reaction_id: int
    comment_id: int
    
class AdoptionCreate(BaseModel):
    pet_id: int
    user_id: int
    latitude: float
    longitude: float
    description: str
    

    
    
class AdoptionCommentSchema(BaseModel):
    comment: str


class AdoptionResponse(BaseModel):
    id: int
    pet: PetBase
    user_id: int
    latitude: float
    longitude: float
    description: Optional[str] = None
    
    class Config:
        from_attributes = True
