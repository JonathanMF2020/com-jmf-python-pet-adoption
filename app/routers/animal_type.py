import os
import shutil
from typing import List
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.animal_type import AnimalType
from app.schemas.animal_type import AnimalTypeBase, AnimalTypeCreate
from app.utils.jwt import JWTManager
from app.config import settings


router = APIRouter(prefix="/animal_type", tags=["AnimalTypes"])

@router.post("/", response_model=AnimalTypeBase)
def create_animal_type(pet: AnimalTypeCreate, db: Session = Depends(get_db), token: str = Depends(JWTManager.verify_token)):
    new_animal_type = AnimalType(
        name=pet.name,
    )
    db.add(new_animal_type)
    db.commit()
    db.refresh(new_animal_type)
    return new_animal_type

@router.get("/", response_model=List[AnimalTypeBase])
def get_animal_type(db: Session = Depends(get_db), token: str = Depends(JWTManager.verify_token)):
    animal_type = db.query(AnimalType).all()  
    return animal_type

@router.post("/save_img/{animal_type_id}")
def save_image(animal_type_id: int, file: UploadFile = File(...), db: Session = Depends(get_db), token: str = Depends(JWTManager.verify_token)):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Formato no permitido")
    if not os.path.exists(settings.UPLOAD_DIR_ANIMAL_TYPE):
        os.makedirs(settings.UPLOAD_DIR_ANIMAL_TYPE)
    
    newname = "animal-type-{}-image.{}".format(animal_type_id, file.content_type.split("/")[-1]) 
    file_path = "{}/{}".format(settings.UPLOAD_DIR_ANIMAL_TYPE,newname)
    
    print(file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    pet = db.query(AnimalType).filter(AnimalType.id == animal_type_id).first()
    pet.filename = newname
    pet.path = file_path
    db.commit()
    db.refresh(pet)
    return {"message": "Update image of AnimalType"}