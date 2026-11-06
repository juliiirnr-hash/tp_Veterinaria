from datetime import datetime
from decimal import Decimal

from pydantic import model_validator
from sqlmodel import SQLModel

from app.modules.mascotas.schemas import MascotaRead


class TurnoPracticaRead(SQLModel):
    practica_id: int
    nombre: str
    precio_unitario: Decimal

    @model_validator(mode="before")
    @classmethod
    def desde_turno_practica(cls, data):
        practica = getattr(data, "practica", None)
        if practica is not None:
            return {
                "practica_id": data.practica_id,
                "nombre": practica.nombre,
                "precio_unitario": data.precio_unitario,
            }
        return data


class TurnoRead(SQLModel):
    id: int
    fecha: datetime
    motivo: str
    total: Decimal
    mascota: MascotaRead
    practicas: list[TurnoPracticaRead]
