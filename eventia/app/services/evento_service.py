import json
from app.repositories.evento_repository import EventoRepository
from app.models.evento import Evento
from app.redis_client import redis_client
from fastapi import HTTPException
import redis
from app.repositories.evento_repository import EventoRepository

CACHE_TTL = 60

class EventoService:
    def __init__(self, repo=None, redis_client=None):
        self.repo = repo or EventoRepository()
        self.redis = redis_client or redis.Redis(host="localhost", port=6379, db=0)

    def get_eventos(self, db):
        cache = self.redis.get("eventos")
        if cache:
            return json.loads(cache)

        eventos = self.repo.listar_todos(db)
        data = [
            {"id_evento": e.id_evento, "nombre": e.nombre, "capacidad": e.capacidad}
            for e in eventos
        ]

        self.redis.set("eventos", json.dumps(data), ex=CACHE_TTL)
        return data

    def crear_evento(self, db, nombre, capacidad):
        evento = self.repo.crear_evento(db, Evento(nombre=nombre, capacidad=capacidad))
        self.redis.delete("eventos")
        return evento

    def actualizar_evento(self, db, evento_id, nuevos_datos):
        actualizado = self.repo.actualizar_evento(db, evento_id, nuevos_datos)
        if not actualizado:
            raise HTTPException(status_code=404, detail="Evento no encontrado")

        self.redis.delete("eventos")
        return actualizado

    def eliminar_evento(self, db, evento_id):
        eliminado = self.repo.eliminar_evento(db, evento_id)
        if not eliminado:
            raise HTTPException(status_code=404, detail="Evento no encontrado")

        self.redis.delete("eventos")
        return eliminado



