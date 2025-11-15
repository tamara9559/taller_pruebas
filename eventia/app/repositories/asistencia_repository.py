from app.models.asistencia import Asistencia

class AsistenciaRepository:
    def crear_asistencia(self, db, asistencia):
        db.add(asistencia)
        db.commit()
        db.refresh(asistencia)
        return asistencia

    def obtener_asistencias(self, db):
        return db.query(Asistencia).all()

    def contar_asistencias_por_evento(self, db, evento_id):
        return db.query(Asistencia).filter(Asistencia.id_evento == evento_id).count()

    def verificar_asistencia_existente(self, db, evento_id, participante_id):
        return db.query(Asistencia).filter(
            Asistencia.id_evento == evento_id,
            Asistencia.id_persona == participante_id
        ).first()

    def obtener_asistencias_por_evento(self, db, evento_id):
        return db.query(Asistencia).filter(Asistencia.id_evento == evento_id).all()


