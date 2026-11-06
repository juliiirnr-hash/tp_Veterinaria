from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_session
from app.modules.turnos import service
from app.modules.turnos.schemas import TurnoRead

router = APIRouter(prefix="/turnos", tags=["turnos"])


@router.get("/{turno_id}", response_model=TurnoRead)
async def obtener_turno(
    turno_id: int, session: AsyncSession = Depends(get_session)
) -> TurnoRead:
    turno = await service.obtener_turno(session, turno_id)
    if not turno:
        raise HTTPException(status_code=404, detail="Turno no encontrado.")
    return turno


@router.delete("/{turno_id}", status_code=204)
async def eliminar_turno(
    turno_id: int, session: AsyncSession = Depends(get_session)
) -> None:
    turno = await service.eliminar_turno(session, turno_id)
    if not turno:
        raise HTTPException(status_code=404, detail="Turno no encontrado.")
    return None
