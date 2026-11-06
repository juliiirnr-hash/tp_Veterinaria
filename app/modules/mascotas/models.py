from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.modules.duenios.models import Duenio
    from app.modules.turnos.models import Turno


class Mascota(SQLModel, table=True):
    __tablename__ = "mascota"

    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(nullable=False)
    especie: str = Field(nullable=False)
    duenio_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("duenio.id", ondelete="RESTRICT"),
            nullable=False,
            index=True,
        )
    )

    duenio: "Duenio" = Relationship(back_populates="mascotas")
    turnos: list["Turno"] = Relationship(back_populates="mascota")
