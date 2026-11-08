from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from sqlmodel import func, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.errores import rechazo
from app.modules.mascotas.models import Mascota
from app.modules.mascotas.schemas import (
    MascotaCreate,
    MascotaPage,
    MascotaRead,
)


async def crear_mascota(session: AsyncSession, datos: MascotaCreate) -> Mascota:
    mascota = Mascota(**datos.model_dump())
    session.add(mascota)
    try:
        await session.commit()
        return mascota
    except IntegrityError as error:
        await session.rollback()
        raise rechazo(
            "No se pudo crear la mascota: el dueño no existe o los datos son inválidos.",
            error,
        )


async def listar_mascotas(session: AsyncSession, page: int, size: int) -> MascotaPage:
    total = (
        await session.exec(select(func.count()).select_from(Mascota))
    ).one()
    pages = max(1, (total + size - 1) // size)
    if page > pages:
        raise HTTPException(
            status_code=422,
            detail=f"La página {page} no existe. La última página disponible es {pages}.",
        )

    consulta = (
        select(Mascota)
        .order_by(Mascota.id)
        .offset((page - 1) * size)
        .limit(size)
    )
    items = list((await session.exec(consulta)).all())
    return MascotaPage(
        items=[MascotaRead.model_validate(mascota) for mascota in items],
        total=total,
        page=page,
        size=size,
        pages=pages,
    )


async def obtener_mascota(session: AsyncSession, mascota_id: int) -> Mascota | None:
    consulta = (
        select(Mascota)
        .where(Mascota.id == mascota_id)
        .options(joinedload(Mascota.duenio))
    )
    resultado = await session.exec(consulta)
    return resultado.first()
