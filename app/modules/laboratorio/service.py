from starlette.concurrency import run_in_threadpool

from app.modules.laboratorio.cliente import consultar_stock


async def obtener_stock(vacuna: str) -> int:
    return await run_in_threadpool(consultar_stock, vacuna)
