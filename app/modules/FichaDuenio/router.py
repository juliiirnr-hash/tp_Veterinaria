from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_session
from app.modules.FichaDuenio import service
from app.modules.FichaDuenio.schemas import (
    FichaDuenioCreate,
    FichaDuenioRead,
    FichaDuenioUpdate,
)

router = APIRouter(prefix="/fichas-duenio", tags=["fichas-duenio"])


@router.post("/", response_model=FichaDuenioRead, status_code=201)
async def crear_ficha_duenio(
    datos: FichaDuenioCreate, session: AsyncSession = Depends(get_session)
):
    return await service.crear_ficha_duenio(session, datos)


@router.get("/duenio/{duenio_id}", response_model=FichaDuenioRead)
async def obtener_ficha_por_duenio(
    duenio_id: int, session: AsyncSession = Depends(get_session)
):
    ficha = await service.obtener_ficha_por_duenio(session, duenio_id)
    if not ficha:
        raise HTTPException(status_code=404, detail="Ficha de dueño no encontrada.")
    return ficha


@router.get("/{ficha_id}", response_model=FichaDuenioRead)
async def obtener_ficha_duenio(
    ficha_id: int, session: AsyncSession = Depends(get_session)
):
    ficha = await service.obtener_ficha_duenio(session, ficha_id)
    if not ficha:
        raise HTTPException(status_code=404, detail="Ficha de dueño no encontrada.")
    return ficha


@router.patch("/{ficha_id}", response_model=FichaDuenioRead)
async def actualizar_ficha_duenio(
    ficha_id: int,
    datos: FichaDuenioUpdate,
    session: AsyncSession = Depends(get_session),
):
    ficha = await service.actualizar_ficha_duenio(session, ficha_id, datos)
    if not ficha:
        raise HTTPException(status_code=404, detail="Ficha de dueño no encontrada.")
    return ficha


@router.delete("/{ficha_id}", status_code=204)
async def eliminar_ficha_duenio(
    ficha_id: int, session: AsyncSession = Depends(get_session)
):
    ficha = await service.eliminar_ficha_duenio(session, ficha_id)
    if not ficha:
        raise HTTPException(status_code=404, detail="Ficha de dueño no encontrada.")
