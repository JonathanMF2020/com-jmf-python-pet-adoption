from pydantic import BaseModel
from datetime import datetime
from app.schemas.user import UserBase

class LogSchema(BaseModel):
    id: int
    service: str
    type: str
    description: str
    timestamp: datetime
    user: UserBase
    