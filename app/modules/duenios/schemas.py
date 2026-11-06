from sqlmodel import SQLModel


class FichaDuenioCreate(SQLModel):
    telefono: str
    direccion: str


class FichaDuenioRead(SQLModel):
    id: int
    duenio_id: int
    telefono: str
    direccion: str


class DuenioCreate(SQLModel):
    nombre: str
    email: str


class DuenioUpdate(SQLModel):
    nombre: str | None = None
    email: str | None = None


class DuenioRead(SQLModel):
    id: int
    nombre: str
    email: str


class DuenioReadWithFicha(SQLModel):
    id: int
    nombre: str
    email: str
    ficha: FichaDuenioRead | None = None
