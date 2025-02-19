from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import Base, engine
from app.routers import auth, pet, adoption, profile, config, log
from app.config import settings

app = FastAPI()

# Crear tablas
Base.metadata.create_all(bind=engine)

# Incluir rutas
app.include_router(auth.router)
app.include_router(pet.router)
app.include_router(adoption.router)
app.include_router(profile.router)
app.include_router(config.router)
app.include_router(log.router)

app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")