from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_session
from app.modules.mascotas import service
from app.modules.mascotas.schemas import (
    MascotaCreate,
    MascotaPage,
    MascotaRead,
    MascotaReadWithDuenio,
)

router = APIRouter(prefix="/mascotas", tags=["mascotas"])


@router.post("/", response_model=MascotaRead, status_code=201)
async def crear_mascota(
    datos: MascotaCreate, session: AsyncSession = Depends(get_session)
) -> MascotaRead:
    return await service.crear_mascota(session, datos)


@router.get("/", response_model=MascotaPage)
async def listar_mascotas(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    session: AsyncSession = Depends(get_session),
) -> MascotaPage:
    return await service.listar_mascotas(session, page, size)


@router.get("/{mascota_id}", response_model=MascotaReadWithDuenio)
async def obtener_mascota(
    mascota_id: int, session: AsyncSession = Depends(get_session)
) -> MascotaReadWithDuenio:
    mascota = await service.obtener_mascota(session, mascota_id)
    if not mascota:
        raise HTTPException(status_code=404, detail="Mascota no encontrada.")
    return mascota
