from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.database import get_session
from app.modules.health import service
from app.modules.health.schemas import SaludLive, SaludReady

router = APIRouter(tags=["health"])


@router.get("/health/live", response_model=SaludLive)
async def live() -> SaludLive:
    return SaludLive(estado="vivo")


@router.get("/health/ready", response_model=SaludReady)
async def ready(session: AsyncSession = Depends(get_session)) -> SaludReady:
    if await service.base_responde(session):
        return SaludReady(estado="listo")
    raise HTTPException(status_code=503, detail="La base de datos no está disponible.")
