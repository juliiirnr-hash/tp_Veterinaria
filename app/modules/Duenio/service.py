from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload, selectinload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.modules.Duenio.models import Duenio
from app.modules.Duenio.schemas import DuenioCreate, DuenioUpdate

async def crear_duenio(session: AsyncSession, datos: DuenioCreate) -> Duenio:
    """Crea un dueño. Si el email ya existe, la base rechaza y responde 409 (RN-01)."""
    duenio = Duenio.model_validate(datos)
    session.add(duenio)
    try:
        await session.commit()
        await session.refresh(duenio)
        return duenio
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=409, 
            detail="El email del dueño ya se encuentra registrado."
        )

async def listar_duenios(session: AsyncSession) -> list[Duenio]:
    return list((await session.exec(select(Duenio).order_by(Duenio.id))).all())

async def obtener_duenio(session: AsyncSession, duenio_id: int) -> Duenio | None:
    return await session.get(Duenio, duenio_id) 

async def actualizar_duenio(session: AsyncSession, duenio_id: int, datos: DuenioUpdate) -> Duenio | None:
    duenio = await session.get(Duenio, duenio_id)
    if not duenio:
        return None

    # Actualizar los campos proporcionados en datos (excluyendo los no enviados)
    for key, value in datos.model_dump(exclude_unset=True).items():
        setattr(duenio, key, value)

    session.add(duenio)
    try:
        await session.commit()
        await session.refresh(duenio)
        return duenio
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=409, 
            detail="El email modificado ya pertenece a otro dueño."
        )

async def leer_duenio_con_ficha(session: AsyncSession, duenio_id: int) -> Duenio | None:
    """Devuelve el dueño con su ficha usando joinedload (relación a uno)."""
    # CORRECCIÓN: joinedload obligatorio para relaciones a uno (sección 4.6)
    consulta = select(Duenio).where(Duenio.id == duenio_id).options(joinedload(Duenio.ficha))
    return await session.exec(consulta).first()

async def leer_duenio_con_mascotas(session: AsyncSession, duenio_id: int) -> Duenio | None:
    """Devuelve el dueño con sus mascotas usando selectinload (colección)."""
    consulta = select(Duenio).where(Duenio.id == duenio_id).options(selectinload(Duenio.mascotas))
    return await session.exec(consulta).first() 

async def leer_mascotas_del_duenio(
    session: AsyncSession, duenio_id: int
) -> list | None:
    """Devuelve las mascotas del dueño (si las tiene)."""
    consulta = select(Duenio).where(Duenio.id == duenio_id).options(selectinload(Duenio.mascotas))
    duenio = await session.exec(consulta).first()
    if duenio:
        return duenio.mascotas
    return None