from decimal import Decimal

from sqlmodel import SQLModel


class TurnoPracticaCreate(SQLModel):
    practica_id: int


class TurnoPracticaRead(SQLModel):
    turno_id: int
    practica_id: int
    nombre_practica: str
    precio_unitario: Decimal
