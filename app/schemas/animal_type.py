
from pydantic import BaseModel


class AnimalTypeBase(BaseModel):
    id: int
    name: str
    filename: str
    path:str
    class Config:
        from_attributes = True
        
class AnimalTypeCreate(BaseModel):
    name: str