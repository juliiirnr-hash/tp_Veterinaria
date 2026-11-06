from sqlmodel import SQLModel

from app.modules.duenios.schemas import DuenioRead


class MascotaCreate(SQLModel):
    nombre: str
    especie: str
    duenio_id: int


class MascotaUpdate(SQLModel):
    nombre: str | None = None
    especie: str | None = None
    duenio_id: int | None = None


class MascotaRead(SQLModel):
    id: int
    nombre: str
    especie: str
    duenio_id: int


class MascotaReadWithDuenio(MascotaRead):
    duenio: DuenioRead


class MascotaPage(SQLModel):
    items: list[MascotaRead]
    total: int
    page: int
    size: int
    pages: int
