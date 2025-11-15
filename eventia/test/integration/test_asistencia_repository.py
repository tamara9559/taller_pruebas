import pytest
from app.models.asistencia import Asistencia
from app.models.participante import Participante
from app.models.evento import Evento
from app.repositories.asistencia_repository import AsistenciaRepository

def test_registrar_asistencia(test_db):
    repo = AsistenciaRepository()

    participante = Participante(nombre="Ana")
    evento = Evento(nombre="Evento X", capacidad=50)
    test_db.add(participante)
    test_db.add(evento)
    test_db.commit()
    test_db.refresh(participante)
    test_db.refresh(evento)

    # Usar los nombres correctos de columnas de Asistencia
    nueva = Asistencia(
        id_persona=participante.id_persona,
        id_evento=evento.id_evento
    )

    test_db.add(nueva)
    test_db.commit()
    test_db.refresh(nueva)

    assert nueva.id_persona == participante.id_persona
    assert nueva.id_evento == evento.id_evento


