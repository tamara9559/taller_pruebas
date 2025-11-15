from app.repositories.participante_repository import ParticipanteRepository
from app.models.participante import Participante


def test_crear_y_listar_participantes(test_db):
    repo = ParticipanteRepository()

    p = Participante(nombre="Carlos")
    repo.crear_participante(test_db, p)

    lista = repo.obtener_participantes(test_db)

    assert len(lista) == 1
    assert lista[0].nombre == "Carlos"
