from app.models.participante import Participante

class ParticipanteRepository:
    def crear_participante(self, db, participante):
        db.add(participante)
        db.commit()
        db.refresh(participante)
        return participante

    def obtener_participantes(self, db):
        return db.query(Participante).all()

    def obtener_por_nombre(self, db, nombre):
        return db.query(Participante).filter(Participante.nombre == nombre).first()

    def actualizar_participante(self, db, participante_id, nuevos_datos):
        participante = db.query(Participante).get(participante_id)
        if participante:
            for key, value in nuevos_datos.items():
                setattr(participante, key, value)
            db.commit()
            db.refresh(participante)
        return participante

    def eliminar_participante(self, db, participante_id):
        participante = db.query(Participante).get(participante_id)
        if participante:
            db.delete(participante)
            db.commit()
        return participante

