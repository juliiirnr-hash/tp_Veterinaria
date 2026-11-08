from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.modules.mascotas.models import Mascota


class Duenio(SQLModel, table=True):
    __tablename__ = "duenio"

    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(nullable=False)
    email: str = Field(unique=True, nullable=False)

    ficha: "FichaDuenio" = Relationship(
        back_populates="duenio",
        sa_relationship_kwargs={"uselist": False, "passive_deletes": True},
    )
    mascotas: list["Mascota"] = Relationship(
        back_populates="duenio",
        sa_relationship_kwargs={"passive_deletes": True},
    )


class FichaDuenio(SQLModel, table=True):
    __tablename__ = "ficha_duenio"

    id: int | None = Field(default=None, primary_key=True)
    duenio_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("duenio.id"),
            nullable=False,
            unique=True,
        )
    )
    telefono: str = Field(nullable=False)
    direccion: str = Field(nullable=False)

    duenio: "Duenio" = Relationship(back_populates="ficha")
