from sqlalchemy.orm import joinedload, selectinload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.modules.turnos.models import Turno, TurnoPractica


async def obtener_turno(session: AsyncSession, turno_id: int) -> Turno | None:
    consulta = (
        select(Turno)
        .where(Turno.id == turno_id)
        .options(
            joinedload(Turno.mascota),
            selectinload(Turno.practicas).selectinload(TurnoPractica.practica),
        )
    )
    return await session.exec(consulta).first()


async def eliminar_turno(session: AsyncSession, turno_id: int) -> Turno | None:
    turno = await session.get(Turno, turno_id)
    if not turno:
        return None

    await session.delete(turno)
    await session.commit()
    return turno
