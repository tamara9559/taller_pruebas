from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ParticipanteCreate(BaseModel):
    nombre: str

class ParticipanteOut(BaseModel):
    id_persona: int
    nombre: str
    class Config:
        orm_mode = True

class EventoCreate(BaseModel):
    nombre: str
    capacidad: int

class EventoOut(BaseModel):
    id_evento: int
    nombre: str
    capacidad: int
    class Config:
        orm_mode = True

class AsistenciaCreate(BaseModel):
    id_persona: int
    id_evento: int

class AsistenciaOut(BaseModel):
    id_asistencia: int
    id_persona: int
    id_evento: int
    fecha_registro: datetime
    class Config:
        orm_mode = True
