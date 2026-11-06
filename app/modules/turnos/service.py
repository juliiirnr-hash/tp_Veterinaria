from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload, selectinload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.errores import rechazo
from app.modules.practicas.models import Practica
from app.modules.turnos.models import Turno, TurnoPractica
from app.modules.turnos.schemas import TurnoCreate


async def obtener_turno(session: AsyncSession, turno_id: int) -> Turno | None:
    consulta = (
        select(Turno)
        .where(Turno.id == turno_id)
        .options(
            joinedload(Turno.mascota),
            selectinload(Turno.practicas).selectinload(TurnoPractica.practica),
        )
    )
    resultado = await session.exec(consulta)
    return resultado.first()


async def eliminar_turno(session: AsyncSession, turno_id: int) -> Turno | None:
    turno = await session.get(Turno, turno_id)
    if not turno:
        return None

    await session.delete(turno)
    await session.commit()
    return turno


async def crear_turno(session: AsyncSession, datos: TurnoCreate) -> Turno:
    ids_practicas = [item.practica_id for item in datos.practicas]
    consulta = select(Practica).where(Practica.id.in_(ids_practicas))
    practicas = (await session.exec(consulta)).all()
    catalogo = {practica.id: practica for practica in practicas}

    faltantes = [pid for pid in ids_practicas if pid not in catalogo]
    if faltantes:
        raise HTTPException(
            status_code=409,
            detail=f"La práctica {faltantes[0]} no existe. No se guardó nada.",
        )

    total = sum(
        (catalogo[item.practica_id].precio for item in datos.practicas),
        Decimal("0.00"),
    )

    turno = Turno(
        mascota_id=datos.mascota_id,
        fecha=datos.fecha,
        motivo=datos.motivo,
        total=total,
    )
    session.add(turno)

    try:
        await session.flush()
        assert turno.id is not None

        for item in datos.practicas:
            practica = catalogo[item.practica_id]
            session.add(
                TurnoPractica(
                    turno_id=turno.id,
                    practica_id=practica.id,
                    precio_unitario=practica.precio,
                )
            )

        await session.commit()

    except IntegrityError as error:
        await session.rollback()
        raise rechazo(
            "No se pudo reservar el turno: la mascota no existe o la práctica está repetida.",
            error,
        )

    turno_creado = await obtener_turno(session, turno.id)
    assert turno_creado is not None
    return turno_creado
