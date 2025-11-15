from fastapi import APIRouter, Depends
from app.database import SessionLocal
from app.services.participante_service import ParticipanteService

router = APIRouter(prefix="/participantes", tags=["Participantes"])
service = ParticipanteService()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def crear(nombre: str, db=Depends(get_db)):
    return service.crear_participante(db, nombre)

@router.get("/")
def listar(db=Depends(get_db)):
    return service.listar(db)

@router.put("/{participante_id}")
def actualizar(participante_id: int, nombre: str, db=Depends(get_db)):
    return service.actualizar_participante(db, participante_id, {"nombre": nombre})

@router.delete("/{participante_id}")
def eliminar(participante_id: int, db=Depends(get_db)):
    return service.eliminar_participante(db, participante_id)

