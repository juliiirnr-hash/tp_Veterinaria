import asyncio
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core import modelos  # noqa: F401
from app.core.database import crear_fabrica_de_sesiones, crear_motor
from app.modules.duenios.models import Duenio, FichaDuenio
from app.modules.mascotas.models import Mascota
from app.modules.practicas.models import Practica
from app.modules.turnos.models import Turno, TurnoPractica


async def sembrar(session: AsyncSession) -> None:
    dueno_ana = Duenio(nombre="Ana García", email="ana@example.com")
    dueno_juan = Duenio(nombre="Juan Pérez", email="juan@example.com")
    session.add_all([dueno_ana, dueno_juan])
    await session.flush()

    ficha = FichaDuenio(
        duenio_id=dueno_ana.id,
        telefono="351-555-0101",
        direccion="Av. Siempre Viva 123",
    )
    mascotas = [
        Mascota(nombre="Toby", especie="perro", duenio_id=dueno_ana.id),
        Mascota(nombre="Mishi", especie="gato", duenio_id=dueno_ana.id),
        Mascota(nombre="Rocky", especie="conejo", duenio_id=dueno_juan.id),
    ]
    practicas = [
        Practica(nombre="Consulta", precio=Decimal("15000.00")),
        Practica(nombre="Vacuna antirrábica", precio=Decimal("12000.00")),
        Practica(nombre="Desparasitación", precio=Decimal("8000.00")),
        Practica(nombre="Radiografía", precio=Decimal("20000.00")),
    ]
    session.add_all([ficha, *mascotas, *practicas])
    await session.flush()

    turno = Turno(
        mascota_id=mascotas[0].id,
        fecha=datetime(2026, 11, 12, 10, 30, tzinfo=timezone(timedelta(hours=-3))),
        motivo="Control anual",
        total=Decimal("27000.00"),
    )
    session.add(turno)
    await session.flush()

    session.add_all(
        [
            TurnoPractica(
                turno_id=turno.id,
                practica_id=practicas[0].id,
                precio_unitario=practicas[0].precio,
            ),
            TurnoPractica(
                turno_id=turno.id,
                practica_id=practicas[1].id,
                precio_unitario=practicas[1].precio,
            ),
        ]
    )
    await session.commit()


async def main() -> None:
    motor = crear_motor()
    fabrica = crear_fabrica_de_sesiones(motor)

    async with motor.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)

    async with fabrica() as session:
        await sembrar(session)

    await motor.dispose()
    print("Base reiniciada: esquema creado y datos iniciales cargados.")


if __name__ == "__main__":
    asyncio.run(main())
