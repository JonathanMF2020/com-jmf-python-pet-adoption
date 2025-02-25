import os
import shutil
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.pet import Pet, PetTag, Tag
from app.models.user import User
from app.schemas.pet import PetCreate, PetBase, PetWithTags, AdoptionEvaluationResponse, AdoptionEvaluationBase
from app.utils.jwt import JWTManager
from app.config import settings

router = APIRouter(prefix="/pets", tags=["Pets"])

@router.post("/save_img/{pet_id}")
def save_image(pet_id: int, file: UploadFile = File(...), db: Session = Depends(get_db), token: str = Depends(JWTManager.verify_token)):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Formato no permitido")
    if not os.path.exists(settings.UPLOAD_DIR):
        os.makedirs(settings.UPLOAD_DIR)
    
    newname = "pet-{}-image.{}".format(pet_id, file.content_type.split("/")[-1]) 
    file_path = "{}/{}".format(settings.UPLOAD_DIR,newname)
    
    print(file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    pet.filename = newname
    pet.path = file_path
    db.commit()
    db.refresh(pet)
    return {"message": "Update image of Pet"}

@router.post("/", response_model=PetBase)
def create_pet(pet: PetCreate, db: Session = Depends(get_db), token: str = Depends(JWTManager.verify_token)):
    new_pet = Pet(
        name=pet.name,
        age=pet.age,
        breed_id=pet.breed_id,
        animal_type_id=pet.animal_type_id,
        description=pet.description,
        available=pet.available,
        gender=pet.gender,
        weight=pet.weight
    )
    db.add(new_pet)
    db.commit()
    db.refresh(new_pet)
    return new_pet

@router.get("/", response_model=List[PetBase])
def get_all_pets(db: Session = Depends(get_db), token: str = Depends(JWTManager.verify_token)):
    pets = db.query(Pet).all()        
    return pets

@router.get("/suggested", response_model=List[PetBase])
def suggested_pets(db: Session = Depends(get_db), token: str = Depends(JWTManager.verify_token)):
    email = token["sub"]
    profile = db.query(User).filter(User.email == email).first()
    
    user_tags = profile.tags  
    
    user_tag_ids = [tag.id for tag in user_tags]
    
    suggested_pets = db.query(Pet).join(Pet.tags).filter(Tag.id.in_(user_tag_ids)).all()
    
    return suggested_pets

@router.get("/{pet_id}", response_model=PetBase)
def get_pet(pet_id: int, db: Session = Depends(get_db), token: str = Depends(JWTManager.verify_token)):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet

@router.put("/{pet_id}", response_model=PetBase)
def update_pet(pet_id: int, pet: PetCreate, db: Session = Depends(get_db), token: str = Depends(JWTManager.verify_token)):
    existing_pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not existing_pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    existing_pet.name = pet.name
    existing_pet.age = pet.age
    existing_pet.breed = pet.breed
    existing_pet.description = pet.description
    existing_pet.available = pet.available
    db.commit()
    db.refresh(existing_pet)
    return existing_pet

@router.delete("/{pet_id}")
def delete_pet(pet_id: int, db: Session = Depends(get_db), token: str = Depends(JWTManager.verify_token)):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    db.delete(pet)
    db.commit()
    return {"message": "Pet deleted successfully"}

@router.post("/pets/{pet_id}/tags")
def add_tags_to_pet(pet_id: int, tags: List[int], db: Session = Depends(get_db), token: str = Depends(JWTManager.verify_token)):
    pet = db.query(Pet).filter(Pet.id == pet_id).first()
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    
    for tag_id in tags:
        tag = db.query(Tag).filter(Tag.id == tag_id).first()
        if tag:
            pet.tags.append(tag)
    
    db.commit()
    return {"message": "Tags added successfully!"}

@router.get("/pets/tags/{tag_id}", response_model=List[PetWithTags])
def get_pets_by_tag(tag_id: int, db: Session = Depends(get_db), token: str = Depends(JWTManager.verify_token)):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    pets = db.query(Pet).join(PetTag).filter(PetTag.tag_id == tag_id).all()
    return pets
