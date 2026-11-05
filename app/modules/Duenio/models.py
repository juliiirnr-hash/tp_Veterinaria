from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel


if TYPE_CHECKING:
    from app.modules.Macota.models import Mascota
    from app.modules.FichaDuenio.models import FichaDuenio


class Duenio(SQLModel, table=True):
    __tablename__ = "duenio"

    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(nullable=False)
    email: str = Field(unique=True, nullable=False)

    mascotas: list["Mascota"] = Relationship(back_populates="duenio")
    ficha: "FichaDuenio | None" = Relationship(
        back_populates="duenio",
        sa_relationship_kwargs={"uselist": False},
    )
