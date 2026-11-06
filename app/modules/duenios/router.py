from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_session
from app.modules.duenios import service
from app.modules.duenios.schemas import (
    DuenioCreate,
    DuenioRead,
    DuenioReadWithFicha,
    DuenioUpdate,
    FichaDuenioCreate,
    FichaDuenioRead,
)
from app.modules.mascotas.schemas import MascotaRead

router = APIRouter(prefix="/duenios", tags=["duenios"])


@router.post("/", response_model=DuenioRead, status_code=201)
async def crear_duenio(
    datos: DuenioCreate, session: AsyncSession = Depends(get_session)
) -> DuenioRead:
    return await service.crear_duenio(session, datos)


@router.get("/{duenio_id}", response_model=DuenioReadWithFicha)
async def obtener_duenio(
    duenio_id: int, session: AsyncSession = Depends(get_session)
) -> DuenioReadWithFicha:
    duenio = await service.obtener_duenio(session, duenio_id)
    if not duenio:
        raise HTTPException(status_code=404, detail="Dueño no encontrado.")
    return duenio


@router.patch("/{duenio_id}", response_model=DuenioReadWithFicha)
async def actualizar_duenio(
    duenio_id: int,
    datos: DuenioUpdate,
    session: AsyncSession = Depends(get_session),
) -> DuenioReadWithFicha:
    duenio = await service.actualizar_duenio(session, duenio_id, datos)
    if not duenio:
        raise HTTPException(status_code=404, detail="Dueño no encontrado.")
    return duenio


@router.delete("/{duenio_id}", status_code=204)
async def eliminar_duenio(
    duenio_id: int, session: AsyncSession = Depends(get_session)
) -> None:
    duenio = await service.eliminar_duenio(session, duenio_id)
    if not duenio:
        raise HTTPException(status_code=404, detail="Dueño no encontrado.")
    return None


@router.post("/{duenio_id}/ficha", response_model=FichaDuenioRead, status_code=201)
async def crear_ficha(
    duenio_id: int,
    datos: FichaDuenioCreate,
    session: AsyncSession = Depends(get_session),
) -> FichaDuenioRead:
    return await service.crear_ficha(session, duenio_id, datos)


@router.get("/{duenio_id}/mascotas", response_model=list[MascotaRead])
async def leer_mascotas_del_duenio(
    duenio_id: int, session: AsyncSession = Depends(get_session)
) -> list[MascotaRead]:
    mascotas = await service.leer_mascotas_del_duenio(session, duenio_id)
    if mascotas is None:
        raise HTTPException(status_code=404, detail="Dueño no encontrado.")
    return mascotas
