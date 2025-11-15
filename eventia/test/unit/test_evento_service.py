import pytest
from app.services.evento_service import EventoService

class FakeEventoRepo:
    def listar_todos(self, db):
        class F:
            id_evento = 1
            nombre = "concierto martin garrix"
            capacidad = 500
        return [F()]

def test_get_eventos(test_db, fake_redis):
    service = EventoService(repo=FakeEventoRepo(), redis_client=fake_redis)

    eventos = service.get_eventos(test_db)

    assert isinstance(eventos, list)
    assert eventos[0]["nombre"] == "concierto DSG"



