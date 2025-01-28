from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.config import Config
from app.schemas.config import ConfigRequest
from app.utils.jwt import JWTManager

router = APIRouter(prefix="/config", tags=["Configurations"])

@router.post("/")
def create_configuration(configRequest: ConfigRequest,db: Session = Depends(get_db), token: str = Depends(JWTManager.verify_token)):
    newconfig = Config(
        key = configRequest.key,
        value = configRequest.value
    )
    db.add(newconfig)
    db.commit()
    db.refresh(newconfig)
    configs = db.query(Config).all()
    return configs