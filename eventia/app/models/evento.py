from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Evento(Base):
    __tablename__ = "eventos"

    id_evento = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    capacidad = Column(Integer, nullable=False)

    # RELACIÓN CORRECTA
    asistencias = relationship(
        "Asistencia",
        back_populates="evento",
        passive_deletes=True
    )

