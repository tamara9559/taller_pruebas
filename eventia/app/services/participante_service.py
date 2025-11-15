import json
from app.repositories.participante_repository import ParticipanteRepository
from app.models.participante import Participante
from app.redis_client import redis_client
from fastapi import HTTPException
import redis

CACHE_TTL = 60

class ParticipanteService:
    def __init__(self, repo=None, redis_client=None):
        self.repo = repo or ParticipanteRepository()
        self.redis = redis_client or redis.Redis(host="localhost", port=6379, db=0)

    def listar(self, db):
        cache = self.redis.get("participantes")
        if cache:
            return json.loads(cache)

        participantes = self.repo.obtener_participantes(db)
        data = [
            {"id_persona": p.id_persona, "nombre": p.nombre}
            for p in participantes
        ]

        self.redis.set("participantes", json.dumps(data), ex=CACHE_TTL)
        return data

    def crear_participante(self, db, nombre):
        if self.repo.obtener_por_nombre(db, nombre):
            raise HTTPException(status_code=409, detail="Participante ya existe")

        nuevo = self.repo.crear_participante(db, Participante(nombre=nombre))
        self.redis.delete("participantes")
        return nuevo

    def actualizar_participante(self, db, participante_id, nuevos_datos):
        actualizado = self.repo.actualizar_participante(db, participante_id, nuevos_datos)
        if not actualizado:
            raise HTTPException(status_code=404, detail="Participante no encontrado")

        self.redis.delete("participantes")

        return {
            "id_persona": actualizado.id_persona,
            "nombre": actualizado.nombre
        }

    def eliminar_participante(self, db, participante_id):
        eliminado = self.repo.eliminar_participante(db, participante_id)
        if not eliminado:
            raise HTTPException(status_code=404, detail="Participante no encontrado")

        self.redis.delete("participantes")
        return {"message": "Participante eliminado correctamente"}




