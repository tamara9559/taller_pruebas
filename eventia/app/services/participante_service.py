import json
from app.repositories.participante_repository import ParticipanteRepository
from app.models.participante import Participante
from app.redis_client import redis_client
from fastapi import HTTPException

class ParticipanteService:
    def __init__(self):
        self.repo = ParticipanteRepository()

    def listar(self, db):
        cache = redis_client.get("participantes")
        if cache:
            return json.loads(cache)

        participantes = self.repo.obtener_participantes(db)
        data = [{"id_persona": p.id_persona, "nombre": p.nombre} for p in participantes]
        redis_client.set("participantes", json.dumps(data))
        return data

    def crear_participante(self, db, nombre):
        if self.repo.obtener_por_nombre(db, nombre):
            raise HTTPException(status_code=409, detail="Participante ya existe")
        participante = Participante(nombre=nombre)
        nuevo = self.repo.crear_participante(db, participante)
        redis_client.delete("participantes")
        return nuevo

    def actualizar_participante(self, db, participante_id, nuevos_datos):
        actualizado = self.repo.actualizar_participante(db, participante_id, nuevos_datos)

        if not actualizado:
            raise HTTPException(status_code=404, detail="Participante no encontrado")

        redis_client.delete("participantes")

        return {
        "id_persona": actualizado.id_persona,
        "nombre": actualizado.nombre
        }


    def eliminar_participante(self, db, participante_id):
        eliminado = self.repo.eliminar_participante(db, participante_id)
    
        if not eliminado:
            raise HTTPException(status_code=404, detail="Participante no encontrado")

        redis_client.delete("participantes")
        return {"message": "Participante eliminado correctamente"}



