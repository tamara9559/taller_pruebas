from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Asistencia(Base):
    __tablename__ = "asistencias"

    id_asistencia = Column(Integer, primary_key=True, autoincrement=True)

    id_evento = Column(
        Integer,
        ForeignKey("eventos.id_evento", ondelete="CASCADE"),
        nullable=False
    )

    id_persona = Column(
        Integer,
        ForeignKey("personas.id_persona", ondelete="CASCADE"),
        nullable=False
    )

    fecha_registro = Column(DateTime, default=datetime.utcnow)

    # RELACIONES SIMÉTRICAS
    evento = relationship("Evento", back_populates="asistencias")
    participante = relationship("Participante", back_populates="asistencias")

    __table_args__ = (
        UniqueConstraint("id_evento", "id_persona", name="uq_evento_participante"),
    )



