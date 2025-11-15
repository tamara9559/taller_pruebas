from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.repositories.evento_repository import EventoRepository
from app.models.evento import Evento

def setup_db():
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

def test_insertar_evento():
    db = setup_db()
    repo = EventoRepository()

    nuevo = Evento(nombre="Prueba", capacidad=150)
    repo.crear_evento(db, nuevo)

    eventos = repo.listar_todos(db)
    assert len(eventos) == 1
    assert eventos[0].nombre == "Prueba"
