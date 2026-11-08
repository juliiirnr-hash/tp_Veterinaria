from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload, selectinload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.errores import CLAVE_FORANEA, codigo_de, rechazo
from app.modules.duenios.models import Duenio, FichaDuenio
from app.modules.duenios.schemas import (
    DuenioCreate,
    DuenioUpdate,
    FichaDuenioCreate,
)


async def crear_duenio(session: AsyncSession, datos: DuenioCreate) -> Duenio:
    duenio = Duenio(**datos.model_dump())
    session.add(duenio)
    try:
        await session.commit()
        return duenio
    except IntegrityError as error:
        await session.rollback()
        raise rechazo("El email del dueño ya se encuentra registrado.", error)


async def obtener_duenio(session: AsyncSession, duenio_id: int) -> Duenio | None:
    consulta = (
        select(Duenio)
        .where(Duenio.id == duenio_id)
        .options(joinedload(Duenio.ficha))
    )
    resultado = await session.exec(consulta)
    return resultado.first()


async def actualizar_duenio(
    session: AsyncSession, duenio_id: int, datos: DuenioUpdate
) -> Duenio | None:
    duenio = await obtener_duenio(session, duenio_id)
    if not duenio:
        return None

    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(duenio, campo, valor)

    session.add(duenio)
    try:
        await session.commit()
        return duenio
    except IntegrityError as error:
        await session.rollback()
        raise rechazo("El email modificado ya pertenece a otro dueño.", error)


async def eliminar_duenio(session: AsyncSession, duenio_id: int) -> Duenio | None:
    duenio = await session.get(Duenio, duenio_id)
    if not duenio:
        return None

    await session.delete(duenio)
    try:
        await session.commit()
        return duenio
    except IntegrityError as error:
        await session.rollback()
        raise rechazo("No se puede borrar un dueño con datos asociados.", error)


async def crear_ficha(
    session: AsyncSession, duenio_id: int, datos: FichaDuenioCreate
) -> FichaDuenio:
    ficha = FichaDuenio(duenio_id=duenio_id, **datos.model_dump())
    session.add(ficha)
    try:
        await session.commit()
        return ficha
    except IntegrityError as error:
        await session.rollback()
        if codigo_de(error) == CLAVE_FORANEA:
            raise HTTPException(status_code=404, detail="Dueño no encontrado.")
        raise rechazo("El dueño ya tiene una ficha registrada.", error)


async def leer_mascotas_del_duenio(session: AsyncSession, duenio_id: int) -> list | None:
    consulta = (
        select(Duenio)
        .where(Duenio.id == duenio_id)
        .options(selectinload(Duenio.mascotas))
    )
    resultado = await session.exec(consulta)
    duenio = resultado.first()
    if not duenio:
        return None
    return duenio.mascotas
