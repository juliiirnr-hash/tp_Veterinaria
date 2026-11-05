from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_session
from app.modules.Duenio import service
from app.modules.Duenio.schemas import (
    DuenioCreate,
    DuenioRead,
    DuenioReadWithFicha,
    DuenioReadWithMascotas,
    DuenioUpdate,
    MascotaRead,
)

router = APIRouter(prefix="/duenios", tags=["duenios"])


@router.post("/", response_model=DuenioRead, status_code=201)
async def crear_duenio(
    datos: DuenioCreate, session: AsyncSession = Depends(get_session)
):
    """Crea un dueño. Si el email ya existe, la base rechaza y responde 409 (RN-01)."""
    return await service.crear_duenio(session, datos)


@router.get("/", response_model=list[DuenioRead])
async def listar_duenios(session: AsyncSession = Depends(get_session)):
    """Lista todos los dueños."""
    return await service.listar_duenios(session)


@router.get("/{duenio_id}", response_model=DuenioRead)
async def obtener_duenio(
    duenio_id: int, session: AsyncSession = Depends(get_session)
):
    """Obtiene un dueño por su ID. Devuelve 404 si no existe."""
    duenio = await service.obtener_duenio(session, duenio_id)
    if not duenio:
        raise HTTPException(status_code=404, detail="Dueño no encontrado.")
    return duenio


@router.patch("/{duenio_id}", response_model=DuenioRead)
async def actualizar_duenio(
    duenio_id: int,
    datos: DuenioUpdate,
    session: AsyncSession = Depends(get_session),
):
    """Actualiza un dueño por su ID. Devuelve 404 si no existe."""
    duenio = await service.actualizar_duenio(session, duenio_id, datos)
    if not duenio:
        raise HTTPException(status_code=404, detail="Dueño no encontrado.")
    return duenio


@router.get("/{duenio_id}/ficha", response_model=DuenioReadWithFicha)
async def leer_duenio_con_ficha(
    duenio_id: int, session: AsyncSession = Depends(get_session)
):
    """Devuelve el dueño con su ficha. Devuelve 404 si no existe."""
    duenio = await service.leer_duenio_con_ficha(session, duenio_id)
    if not duenio:
        raise HTTPException(status_code=404, detail="Dueño no encontrado.")
    return duenio


@router.get("/{duenio_id}/mascotas", response_model=DuenioReadWithMascotas)
async def leer_duenio_con_mascotas(
    duenio_id: int, session: AsyncSession = Depends(get_session)
):
    """Devuelve el dueño con sus mascotas. Devuelve 404 si no existe."""
    duenio = await service.leer_duenio_con_mascotas(session, duenio_id)
    if not duenio:
        raise HTTPException(status_code=404, detail="Dueño no encontrado.")
    return duenio


@router.get("/{duenio_id}/mascotas/lista", response_model=list[MascotaRead])
async def leer_mascotas_del_duenio(
    duenio_id: int, session: AsyncSession = Depends(get_session)
):
    """Devuelve las mascotas del dueño (si las tiene)."""
    mascotas = await service.leer_mascotas_del_duenio(session, duenio_id)
    if mascotas is None:
        raise HTTPException(status_code=404, detail="Dueño no encontrado.")
    return mascotas