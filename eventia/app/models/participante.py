from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Participante(Base):
    __tablename__ = "personas"

    id_persona = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)

    # RELACIÓN CORRECTA
    asistencias = relationship("Asistencia", back_populates="participante")



    
