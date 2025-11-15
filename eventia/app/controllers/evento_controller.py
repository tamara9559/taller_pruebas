from fastapi import APIRouter, Depends
from app.database import SessionLocal
from app.services.evento_service import EventoService

router = APIRouter(prefix="/eventos", tags=["Eventos"])
service = EventoService()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def listar_eventos(db=Depends(get_db)):
    return service.get_eventos(db)

@router.post("/")
def crear_evento(nombre: str, capacidad: int, db=Depends(get_db)):
    return service.crear_evento(db, nombre, capacidad)

@router.put("/{evento_id}")
def actualizar_evento(evento_id: int, nombre: str, capacidad: int, db=Depends(get_db)):
    return service.actualizar_evento(db, evento_id, {"nombre": nombre, "capacidad": capacidad})

@router.delete("/{evento_id}")
def eliminar_evento(evento_id: int, db=Depends(get_db)):
    return service.eliminar_evento(db, evento_id)

