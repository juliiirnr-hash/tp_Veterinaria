from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, Integer, Numeric
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.modules.mascotas.models import Mascota
    from app.modules.practicas.models import Practica


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
    fecha: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False))
    motivo: str = Field(nullable=False)
    total: Decimal = Field(sa_column=Column(Numeric(12, 2), nullable=False))

    mascota: "Mascota" = Relationship(back_populates="turnos")
    practicas: list["TurnoPractica"] = Relationship(
        back_populates="turno",
        sa_relationship_kwargs={"passive_deletes": True},
    )


class TurnoPractica(SQLModel, table=True):
    __tablename__ = "turno_practica"
    __table_args__ = (
        CheckConstraint(
            "precio_unitario > 0",
            name="ck_turno_practica_precio_unitario_positivo",
        ),
    )

    turno_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("turno.id", ondelete="CASCADE"),
            primary_key=True,
        )
    )
    practica_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("practica.id"),
            primary_key=True,
            index=True,
        )
    )
    precio_unitario: Decimal = Field(
        sa_column=Column(Numeric(10, 2), nullable=False)
    )

    turno: "Turno" = Relationship(back_populates="practicas")
    practica: "Practica" = Relationship(back_populates="turnos")
