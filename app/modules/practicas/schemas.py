from decimal import Decimal

from sqlmodel import Field, SQLModel


class PracticaCreate(SQLModel):
    nombre: str
    precio: Decimal = Field(gt=0)


class PracticaUpdate(SQLModel):
    nombre: str | None = None
    precio: Decimal | None = Field(default=None, gt=0)


class PracticaRead(SQLModel):
    id: int
    nombre: str
    precio: Decimal
