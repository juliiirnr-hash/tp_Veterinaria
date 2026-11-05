from sqlmodel import SQLModel
from typing import Optional

# ─── Ficha Duenio (Necesaria para el Dueño) ──────────────────────────────
class FichaDuenioRead(SQLModel):
    id: int
    telefono: str
    direccion: str

# ─── Duenio ───────────────────────────────────────────────────────────────
class DuenioCreate(SQLModel):
    nombre: str
    email: str

class DuenioRead(SQLModel):
    id: int
    nombre: str
    email: str

class DuenioUpdate(SQLModel):
    nombre: str | None = None
    email: str | None = None

# Para GET /duenios/{id} y PATCH /duenios/{id} (Devuelven el dueño con su ficha)
class DuenioReadWithFicha(SQLModel):
    id: int
    nombre: str
    email: str
    ficha: Optional[FichaDuenioRead] = None  # Puede no tener ficha cargada aún

# Para cuando necesites mostrar las mascotas del dueño
class DuenioReadWithMascotas(SQLModel):
    id: int
    nombre: str
    email: str
    mascotas: list["MascotaRead"] = [] 

class MascotaRead(SQLModel):
    id: int
    nombre: str
    especie: str
    duenio_id: int

