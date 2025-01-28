from typing import List
from pydantic import BaseModel

from app.schemas.pet import TagSchema


class ProfileBase(BaseModel):
    user_id: int
    
class PermissionsBase(BaseModel):
    id: int
    name: str
    
class ProfileRequestBase(BaseModel):
    id: int
    username: str
    email: str
    tags: List[TagSchema]
    permissions: List[PermissionsBase]
    
    class Config:
        orm_mode = True
    

    