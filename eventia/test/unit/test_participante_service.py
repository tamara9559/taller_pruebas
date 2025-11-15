import pytest
from app.services.participante_service import ParticipanteService
from app.repositories.participante_repository import ParticipanteRepository
from app.models.participante import Participante

def test_listar_participantes(test_db):
    repo = ParticipanteRepository()
    service = ParticipanteService()

    # Insertar participante de prueba
    p = Participante(nombre="Juan")
    test_db.add(p)
    test_db.commit()
    test_db.refresh(p)

    from app.redis_client import redis_client
    redis_client.delete("participantes")  # limpiar cache
    participantes = service.listar(test_db)

    # Verificaciones
    assert isinstance(participantes, list)
    # Como el método devuelve diccionarios
    assert any(pt["id_persona"] == p.id_persona for pt in participantes)
    assert any(pt["nombre"] == "Juan" for pt in participantes)






