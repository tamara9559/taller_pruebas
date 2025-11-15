from fastapi import HTTPException
from app.repositories.asistencia_repository import AsistenciaRepository
from app.models.asistencia import Asistencia
from app.models.evento import Evento
from app.redis_client import redis_client
import json

CACHE_TTL = 60  # segundos

class AsistenciaService:
    def __init__(self):
        self.repo = AsistenciaRepository()

    def registrar(self, db, participante_id, evento_id):
        # Verificar duplicado
        if self.repo.verificar_asistencia_existente(db, evento_id, participante_id):
            raise HTTPException(status_code=409, detail="Asistencia ya registrada")

        # Verificar capacidad
        evento = db.query(Evento).get(evento_id)
        if not evento:
            raise HTTPException(status_code=404, detail="Evento no encontrado")
        if self.repo.contar_asistencias_por_evento(db, evento_id) >= evento.capacidad:
            raise HTTPException(status_code=400, detail="Evento lleno")

        asistencia = Asistencia(id_persona=participante_id, id_evento=evento_id)
        nueva = self.repo.crear_asistencia(db, asistencia)

        # Limpiar cache de asistencia y estadísticas
        redis_client.delete(f"asistencias_evento_{evento_id}")
        redis_client.delete("estadisticas_ocupacion")

        return nueva

    def get_asistencias(self, db, evento_id: int = None):
        # Cache por evento
        cache_key = f"asistencias_evento_{evento_id}" if evento_id else "asistencias_todas"
        cached = redis_client.get(cache_key)
        if cached:
            return json.loads(cached)

        if evento_id:
            asistencias = self.repo.obtener_asistencias_por_evento(db, evento_id)
        else:
            asistencias = self.repo.obtener_asistencias(db)

        data = [{"id_asistencia": a.id_asistencia,
                 "id_persona": a.id_persona,
                 "id_evento": a.id_evento,
                 "fecha_registro": a.fecha_registro.isoformat()} for a in asistencias]

        redis_client.set(cache_key, json.dumps(data), ex=CACHE_TTL)
        return data

    def obtener_estadisticas(self, db):
        cache_key = "estadisticas_ocupacion"
        cached = redis_client.get(cache_key)
        if cached:
            return json.loads(cached)

        from app.models.evento import Evento
        eventos = db.query(Evento).all()
        stats = []
        for e in eventos:
            ocupacion = self.repo.contar_asistencias_por_evento(db, e.id_evento)
            porcentaje = (ocupacion / e.capacidad) * 100 if e.capacidad else 0
            stats.append({
                "id_evento": e.id_evento,
                "nombre": e.nombre,
                "capacidad": e.capacidad,
                "asistencias": ocupacion,
                "ocupacion_pct": round(porcentaje, 2)
            })

        redis_client.set(cache_key, json.dumps(stats), ex=CACHE_TTL)
        return stats



