from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.user import Token, UserCreate, UserLogin
from app.utils.hashing import Hash
from app.utils.jwt import JWTManager

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = Hash.bcrypt(user.password)
    new_user = User(email=user.email, username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"}

@router.post("/login", response_model=Token)
def login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not Hash.verify(db_user.hashed_password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = JWTManager.create_access_token({"sub": db_user.email})
    return {"access_token": token, "token_type": "bearer"}
