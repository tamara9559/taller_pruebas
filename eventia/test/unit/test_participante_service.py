import pytest
from app.services.participante_service import ParticipanteService
from app.models.participante import Participante

def test_listar_participantes(test_db, fake_redis):
    service = ParticipanteService(redis_client=fake_redis)

    p = Participante(nombre="Juan")
    test_db.add(p)
    test_db.commit()
    test_db.refresh(p)

    participantes = service.listar(test_db)

    assert isinstance(participantes, list)
    assert any(pt["id_persona"] == p.id_persona for pt in participantes)
    assert any(pt["nombre"] == "Juan" for pt in participantes)






