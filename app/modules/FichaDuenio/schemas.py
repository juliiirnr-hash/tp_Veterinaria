from sqlmodel import SQLModel


class FichaDuenioCreate(SQLModel):
    """Datos necesarios para crear la ficha de un dueño.

    ``duenio_id`` identifica al dueño al que pertenece la ficha. La base de
    datos garantiza que cada dueño tenga como máximo una ficha mediante una
    restricción UNIQUE sobre esa columna.
    """

    duenio_id: int
    telefono: str
    direccion: str


class FichaDuenioRead(SQLModel):
    """Datos que la API devuelve al consultar una ficha de dueño."""

    id: int
    duenio_id: int
    telefono: str
    direccion: str


class FichaDuenioUpdate(SQLModel):
    """Campos opcionales para actualizar una ficha existente."""

    telefono: str | None = None
    direccion: str | None = None