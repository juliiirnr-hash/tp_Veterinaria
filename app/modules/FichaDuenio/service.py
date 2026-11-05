from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.modules.FichaDuenio.models import FichaDuenio
from app.modules.FichaDuenio.schemas import FichaDuenioCreate, FichaDuenioUpdate


async def crear_ficha_duenio(
    session: AsyncSession, datos: FichaDuenioCreate
) -> FichaDuenio:
    ficha = FichaDuenio.model_validate(datos)
    session.add(ficha)
    try:
        await session.commit()
        await session.refresh(ficha)
        return ficha
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=409,
            detail="El dueño no existe o ya tiene una ficha registrada.",
        )


async def obtener_ficha_duenio(
    session: AsyncSession, ficha_id: int
) -> FichaDuenio | None:
    return await session.get(FichaDuenio, ficha_id)


async def listar_fichas_duenio(session: AsyncSession) -> list[FichaDuenio]:
    consulta = select(FichaDuenio).order_by(FichaDuenio.id)
    return list((await session.exec(consulta)).all())


async def obtener_ficha_por_duenio(
    session: AsyncSession, duenio_id: int
) -> FichaDuenio | None:
    consulta = select(FichaDuenio).where(FichaDuenio.duenio_id == duenio_id)
    return await session.exec(consulta).first()


async def actualizar_ficha_duenio(
    session: AsyncSession,
    ficha_id: int,
    datos: FichaDuenioUpdate,
) -> FichaDuenio | None:
    ficha = await session.get(FichaDuenio, ficha_id)
    if not ficha:
        return None

    cambios = datos.model_dump(exclude_unset=True)
    for campo, valor in cambios.items():
        setattr(ficha, campo, valor)

    session.add(ficha)
    await session.commit()
    await session.refresh(ficha)
    return ficha


async def eliminar_ficha_duenio(
    session: AsyncSession, ficha_id: int
) -> FichaDuenio | None:
    ficha = await session.get(FichaDuenio, ficha_id)
    if not ficha:
        return None

    await session.delete(ficha)
    await session.commit()
    return ficha