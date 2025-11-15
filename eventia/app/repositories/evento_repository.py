from app.models.evento import Evento

class EventoRepository:
    def crear_evento(self, db, evento):
        db.add(evento)
        db.commit()
        db.refresh(evento)
        return evento

    def listar_todos(self, db):
        return db.query(Evento).all()

    def obtener_por_id(self, db, evento_id):
        return db.query(Evento).get(evento_id)

    def actualizar_evento(self, db, evento_id, nuevos_datos):
        evento = db.query(Evento).get(evento_id)
        if evento:
            for key, value in nuevos_datos.items():
                setattr(evento, key, value)
            db.commit()
            db.refresh(evento)
        return evento

    def eliminar_evento(self, db, evento_id):
        evento = db.query(Evento).get(evento_id)
        if evento:
            db.delete(evento)
            db.commit()
        return evento


