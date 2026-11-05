from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Integer, Numeric
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.modules.Macota.models import Mascota
    from app.modules.TurnoPractica.models import TurnoPractica


class Turno(SQLModel, table=True):
    __tablename__ = "turno"
    __table_args__ = (
        CheckConstraint("total >= 0", name="ck_turno_total_no_negativo"),
    )

    id: int | None = Field(default=None, primary_key=True)
    mascota_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("mascota.id"),
            nullable=False,
            index=True,
        )
    )
    fecha: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False),
    )
    motivo: str = Field(nullable=False)
    total: Decimal = Field(
        sa_column=Column(Numeric(12, 2), nullable=False),
    )

    mascota: "Mascota" = Relationship(back_populates="turnos")
    practicas: list["TurnoPractica"] = Relationship(
        back_populates="turno",
        sa_relationship_kwargs={"passive_deletes": True},
    )