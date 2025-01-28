from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.pet import Tag
from app.models.user import User
from app.models.permission import Permission, ProfilePermissions
from app.schemas.profile import ProfileBase, ProfileRequestBase
from app.utils.fastlog import FastLog
from app.utils.jwt import JWTManager
from datetime import date
from sqlalchemy.sql import func


router = APIRouter(prefix="/profile", tags=["Profile"])

@router.get("/", response_model=ProfileRequestBase)
def get_profile(db: Session = Depends(get_db), token: str = Depends(JWTManager.verify_token)):
    email = token["sub"]
    profile = db.query(User).filter(User.email == email).first()
    return profile

@router.get("/all", response_model=List[ProfileRequestBase])
def get_all_profiles(db: Session = Depends(get_db), token: str = Depends(JWTManager.verify_token)):
    profile = db.query(User).all()
    return profile

@router.post("/assign-admin")
def assign_admin(request: ProfileBase,db: Session = Depends(get_db), token: str = Depends(JWTManager.verify_token)):
    email = token["sub"]
    profileUser = db.query(User).filter(User.email == email).first()
    
    profile = db.query(User).filter(User.id == request.user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Not found user")
    FastLog.LogInformation("/assign-admin","Se acaba de asignar de admin a {}".format(profile.username),profileUser.id, db)
    profile.is_admin = True
    db.commit()
    db.refresh(profile)
    return profile
    
@router.post("/assign-tags")
def assign_tags(tags: List[int], db: Session = Depends(get_db), token: str = Depends(JWTManager.verify_token)):
    email = token["sub"]
    profile = db.query(User).filter(User.email == email).first()
    for tag_id in tags:
        tag = db.query(Tag).filter(Tag.id == tag_id).first()
        profile.tags.append(tag)
    db.commit()
    return {"message": "Tags added successfully!"}

@router.post("/assign-permission/{user_id}")
def assign_permissions(user_id: int,permissions: List[int], db: Session = Depends(get_db), token: str = Depends(JWTManager.verify_token)):
    email = token["sub"]
    profile = db.query(User).filter(User.email == email).first()
    if profile.is_admin == False:
        raise HTTPException(status_code=404, detail="You no are admin")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for permission_id in permissions:
        permission = db.query(Permission).filter(Permission.id == permission_id).filter(Permission.available == True).first()
        if not permission:
            raise HTTPException(status_code=404, detail="Permission not found")
        else:
            
            FastLog.LogInformation("/assign-permission","Se acaba de asignar el permiso {} a {}".format(permission.name,user.username),profile.id, db)
            permissionP = db.query(ProfilePermissions).filter(ProfilePermissions.permision_id == permission_id).filter(ProfilePermissions.user_id == user.id).first()
            if not permissionP:
                newpermission = ProfilePermissions(
                    timestamp = func.now(),
                    user_id = user.id,
                    permision_id = permission.id
                )
                db.add(newpermission)
                db.commit()
                db.refresh(newpermission)
                return {"message": "Permissions added successfully!"}
            else:
                return {"message": "A permission is already included in the account"}


    
    