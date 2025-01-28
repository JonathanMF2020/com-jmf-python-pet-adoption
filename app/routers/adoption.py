from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from app.database import get_db
from app.models.adoption import Adoption, AdoptionComment, AdoptionCommentReaction, Reaction
from app.models.pet import Pet
from app.models.user import User
from app.schemas.adoption import AdoptionCommentBaseSchema, AdoptionCommentSchema, AdoptionCreate, AdoptionResponse, AdoptationEnd, AdoptionGet, ReactionInComment, ReactionResponse, ReactionsGet
from app.utils.jwt import JWTManager

router = APIRouter(prefix="/adoptions", tags=["Adoptions"])

@router.post("/", response_model=AdoptionResponse)
def create_adoption(adoption: AdoptionCreate, db: Session = Depends(get_db), token: str = Depends(JWTManager.verify_token)):
    pet = db.query(Pet).filter(Pet.id == adoption.pet_id, Pet.available == True).first()
    if not pet:
        raise HTTPException(status_code=400, detail="Pet not available for adoption")
    user = db.query(User).filter(User.id == adoption.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    new_adoption = Adoption(
        pet_id=adoption.pet_id,
        user_id=adoption.user_id,
        latitude=adoption.latitude,
        longitude=adoption.longitude,
        description=adoption.description,
        available=1
    )

    db.add(new_adoption)
    db.commit()
    db.refresh(new_adoption)
    return new_adoption

@router.post("/end-adoption", response_model=AdoptionResponse)
def end_adoption(adoption: AdoptationEnd, db: Session = Depends(get_db), token: str = Depends(JWTManager.verify_token)):
    pet = db.query(Pet).filter(Pet.id == adoption.pet_id, Pet.available == True).first()
    if not pet:
        raise HTTPException(status_code=400, detail="Pet not available for adoption")
    user = db.query(User).filter(User.id == adoption.adopter_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    adopion = db.query(Adoption).filter(Adoption.pet_id == adoption.pet_id).first()
    if not adopion:
        raise HTTPException(status_code=400, detail="Adoption not founded")
    
    adopion.available = False
    adopion.adoption_date = date.today()
    adopion.adopter_id = adoption.adopter_id
    # Marcar al pet como no disponible
    pet.available = False
    db.add(pet)
    db.add(adopion)
    db.commit()
    db.refresh(pet)
    db.refresh(adopion)
    return adopion

@router.get("/reactions", response_model=List[ReactionResponse])
def get_reactions(db: Session = Depends(get_db), token: str = Depends(JWTManager.verify_token)):
    reactions = db.query(Reaction).all()
    return reactions


@router.post("/reaction", response_model=AdoptionCommentBaseSchema)
def insert_reaction_comment(request: ReactionInComment, db: Session = Depends(get_db), token: str = Depends(JWTManager.verify_token)):
    comment = db.query(AdoptionComment).filter(AdoptionComment.id == request.comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    reaction = db.query(Reaction).filter(Reaction.id == request.reaction_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Reaction not found")
    
    email = token["sub"]
    profile = db.query(User).filter(User.email == email).first()
    reaction_comment = AdoptionCommentReaction(
        user_id = profile.id,
        comment_id = comment.id,
        reaction_id = reaction.id
    )
    db.add(reaction_comment)
    db.commit()
    db.refresh(reaction_comment)
    comment = db.query(AdoptionComment).filter(AdoptionComment.id == request.comment_id).first()
    return comment

@router.get("/", response_model=List[AdoptionGet])
def get_all_adoptions(db: Session = Depends(get_db), token: str = Depends(JWTManager.verify_token)):
    adoptions = db.query(Adoption).all()
    return adoptions

@router.get("/{adoption_id}", response_model=AdoptionResponse)
def get_adoption(adoption_id: int, db: Session = Depends(get_db), token: str = Depends(JWTManager.verify_token)):
    adoption = db.query(Adoption).filter(Adoption.id == adoption_id).first()
    if not adoption:
        raise HTTPException(status_code=404, detail="Adoption not found")
    return adoption

@router.post("/comment/{adoption_id_2}")
def comment_adoption(adoption_id_2: int, adoption: AdoptionCommentSchema, db: Session = Depends(get_db), token: str = Depends(JWTManager.verify_token)):
    email = token["sub"]
    profile = db.query(User).filter(User.email == email).first()
    new_comment = AdoptionComment(
        comment = adoption.comment,
        adoption_id = adoption_id_2,
        user_id = profile.id
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return {"message": "Comment added successfully!"}

