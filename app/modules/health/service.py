import logging

from sqlalchemy import text
from sqlmodel.ext.asyncio.session import AsyncSession

log = logging.getLogger("uvicorn.error")


async def base_responde(session: AsyncSession) -> bool:
    try:
        await session.execute(text("SELECT 1"))
        return True
    except Exception as exc:
        log.warning("La base no respondió al health check: %s", exc)
        return False
