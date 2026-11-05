from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.modules.Duenio.models import Duenio


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