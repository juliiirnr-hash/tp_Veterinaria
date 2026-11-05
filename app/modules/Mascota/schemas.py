from sqlmodel import SQLModel
from typing import Optional
from app.modules.Duenio.schemas import DuenioRead

class MascotaCreate(SQLModel):
    nombre: str
    especie: str
    duenio_id: int

class MascotaRead(SQLModel):
    id: int
    nombre: str
    especie: str
    duenio_id: int

class MascotaUpdate(SQLModel):
    nombre: str | None = None
    especie: str | None = None
    duenio_id: int | None = None    

class MascotaReadWithDuenio(SQLModel):
    id: int
    nombre: str
    especie: str
    duenio_id: int
    duenio: Optional["DuenioRead"] = None  # Puede no tener dueño cargado aún

