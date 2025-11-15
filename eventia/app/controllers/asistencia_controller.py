from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.services.asistencia_service import AsistenciaService
from app.schemas import AsistenciaCreate, AsistenciaOut
from typing import List

router = APIRouter(prefix="/asistencias", tags=["Asistencias"])
service = AsistenciaService()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=AsistenciaOut)
def registrar(asistencia: AsistenciaCreate, db: Session = Depends(get_db)):
    return service.registrar(db, asistencia.id_persona, asistencia.id_evento)

@router.get("/", response_model=List[AsistenciaOut])
def listar(evento_id: int = None, db: Session = Depends(get_db)):
    return service.get_asistencias(db, evento_id)

@router.get("/estadisticas")
def estadisticas(db: Session = Depends(get_db)):
    return service.obtener_estadisticas(db)


