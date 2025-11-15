import pytest
from app.services.asistencia_service import AsistenciaService
from app.repositories.asistencia_repository import AsistenciaRepository
from app.models.participante import Participante
from app.models.evento import Evento
from app.models.asistencia import Asistencia

def test_listar_asistencias(test_db, fake_redis):
    service = AsistenciaService(redis_client=fake_redis)

    participante = Participante(nombre="Ana")
    evento = Evento(nombre="Evento X", capacidad=50)
    test_db.add(participante)
    test_db.add(evento)
    test_db.commit()
    test_db.refresh(participante)
    test_db.refresh(evento)

    asistencia = Asistencia(
        id_persona=participante.id_persona,
        id_evento=evento.id_evento
    )
    test_db.add(asistencia)
    test_db.commit()
    test_db.refresh(asistencia)

    asistencias = service.get_asistencias(test_db, evento.id_evento)

    assert len(asistencias) == 1
    assert asistencias[0]["id_persona"] == participante.id_persona

