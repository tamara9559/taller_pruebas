import json
from app.repositories.evento_repository import EventoRepository
from app.models.evento import Evento
from app.redis_client import redis_client
from fastapi import HTTPException

class EventoService:
    def __init__(self, repo=None):
        self.repo = repo or EventoRepository()

    def get_eventos(self, db):
        cache = redis_client.get("eventos")
        if cache:
            return json.loads(cache)

        eventos = self.repo.listar_todos(db)
        data = [{"id_evento": e.id_evento, "nombre": e.nombre, "capacidad": e.capacidad} for e in eventos]
        redis_client.set("eventos", json.dumps(data))
        return data

    def crear_evento(self, db, nombre, capacidad):
        evento = Evento(nombre=nombre, capacidad=capacidad)
        nuevo = self.repo.crear_evento(db, evento)
        redis_client.delete("eventos")
        return nuevo

    def actualizar_evento(self, db, evento_id, nuevos_datos):
        actualizado = self.repo.actualizar_evento(db, evento_id, nuevos_datos)
        if not actualizado:
            raise HTTPException(status_code=404, detail="Evento no encontrado")
        redis_client.delete("eventos")
        return actualizado

    def eliminar_evento(self, db, evento_id):
        eliminado = self.repo.eliminar_evento(db, evento_id)
        if not eliminado:
            raise HTTPException(status_code=404, detail="Evento no encontrado")
        redis_client.delete("eventos")
        return eliminado


