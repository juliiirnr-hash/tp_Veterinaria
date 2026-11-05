from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, Numeric
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.modules.Practica.models import Practica
    from app.modules.Turno.models import Turno


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
        sa_column=Column(Numeric(10, 2), nullable=False),
    )

    turno: "Turno" = Relationship(back_populates="practicas")
    practica: "Practica" = Relationship(back_populates="turnos")