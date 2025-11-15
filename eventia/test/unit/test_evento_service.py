import pytest
from app.services.evento_service import EventoService

class FakeEventoRepo:
    def list(self, db):
        return [{"id": 1, "nombre": "Evento Test"}]

def test_get_eventos(test_db):
    service = EventoService()
    service.repo = FakeEventoRepo()

    eventos = service.get_eventos(test_db)
    assert isinstance(eventos, list)
    assert eventos[0]["nombre"] == "concierto martin garrix"


