import asyncio
import os
import sys
import time

import httpx

BASE = os.getenv("BASE_URL", "http://127.0.0.1:8000")


async def main() -> int:
    async with httpx.AsyncClient(base_url=BASE, timeout=30) as cliente:

        async def stock(vacuna: str):
            inicio = time.perf_counter()
            respuesta = await cliente.get(f"/laboratorio/stock/{vacuna}")
            respuesta.raise_for_status()
            return vacuna, respuesta.json(), time.perf_counter() - inicio

        async def salud():
            await asyncio.sleep(0.15)
            inicio = time.perf_counter()
            respuesta = await cliente.get("/health/live")
            respuesta.raise_for_status()
            return respuesta.json(), time.perf_counter() - inicio

        inicio = time.perf_counter()
        resultados = await asyncio.gather(
            stock("rabia"),
            stock("a"),
            stock("ccc"),
            salud(),
        )
        total = time.perf_counter() - inicio

    for vacuna, cuerpo, demora in resultados[:3]:
        print(f"stock {vacuna}: {cuerpo} en {demora:.2f}s")

    cuerpo_salud, demora_salud = resultados[3]
    print(f"health/live durante las consultas: {cuerpo_salud} en {demora_salud:.3f}s")
    print(f"tiempo total de las tres consultas: {total:.2f}s")

    if total >= 2.0 or demora_salud >= 0.5:
        print("C-09 FALLA: las consultas se bloquearon entre sí.")
        return 1

    print("C-09 OK: las tres consultas corren en paralelo y health/live responde de inmediato.")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
