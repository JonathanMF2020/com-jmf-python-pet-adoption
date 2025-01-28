from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.log import Log
from app.schemas.log import LogSchema
from app.utils.jwt import JWTManager

router = APIRouter(prefix="/logs", tags=["Logs"])

@router.get("/", response_model=List[LogSchema])
def get_all_logs(db: Session = Depends(get_db), token: str = Depends(JWTManager.verify_token)):
    # Obtenemos todos los perritos con sus etiquetas asociadas
    pets = db.query(Log).all()        
    return pets