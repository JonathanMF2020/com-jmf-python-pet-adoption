
from typing import Optional
from pydantic import BaseModel


class AnimalTypeBase(BaseModel):
    id: int
    name: str
    filename: Optional[str] = None
    path:Optional[str] = None
    class Config:
        from_attributes = True
        
class AnimalTypeCreate(BaseModel):
    name: str