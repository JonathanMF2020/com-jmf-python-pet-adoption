from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.config import settings

class JWTManager:
    @staticmethod
    def create_access_token(data: dict) -> str:
        """
        Crea un token de acceso JWT con un tiempo de expiración definido.
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_access_token(token: str) -> dict:
        """
        Verifica la validez de un token de acceso JWT y retorna su contenido.
        """
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            return payload
        except JWTError:
            return None
        
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
    @staticmethod
    def verify_token(token: str = Depends(oauth2_scheme)):
        try:
            
            payload = JWTManager.verify_access_token(token)
            if payload is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token or expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return payload
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token or expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
