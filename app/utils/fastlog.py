from app.models.log import Log
from app.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends


class FastLog:
    @staticmethod
    def LogInformation(service: str,text: str, user_id: int,db: Session):
        log = Log(
            service = service,
            type = "Information",
            description = text,
            user_id = user_id
        )
        db.add(log)
        db.commit()
        db.refresh(log)
       
    @staticmethod    
    def LogError(service: str,text: str, user_id: int,db: Session):
        log = Log(
            service = service,
            type = "Error",
            description = text,
            user_id = user_id
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        
        
        