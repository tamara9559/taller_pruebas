from fastapi import FastAPI
from app.controllers.evento_controller import router as evento_router
from app.controllers.participante_controller import router as participante_router
from app.controllers.asistencia_controller import router as asistencia_router
from app.database import engine, Base
from app.models import Participante, Evento, Asistencia
import os

app = FastAPI()


@app.on_event("startup")
def startup():
    # Solo crear tablas si NO estamos en testing
    if os.getenv("ENV") != "TEST":
        Base.metadata.create_all(bind=engine)


# Routers
app.include_router(evento_router)
app.include_router(participante_router)
app.include_router(asistencia_router)


