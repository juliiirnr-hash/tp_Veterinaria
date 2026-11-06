from contextlib import asynccontextmanager

from fastapi import FastAPI

import app.core.modelos  # noqa: F401
from app.core.database import crear_fabrica_de_sesiones, crear_motor
from app.modules.duenios.router import router as duenios_router
from app.modules.health.router import router as health_router
from app.modules.mascotas.router import router as mascotas_router
from app.modules.practicas.router import router as practicas_router
from app.modules.turnos.router import router as turnos_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    motor = crear_motor()
    app.state.motor = motor
    app.state.fabrica_de_sesiones = crear_fabrica_de_sesiones(motor)
    yield
    await motor.dispose()


app = FastAPI(
    title="API Veterinaria",
    version="1.0.0",
    description="API asincrónica para la veterinaria de barrio (Programación III - UTN).",
    lifespan=lifespan,
)

app.include_router(health_router)
app.include_router(duenios_router)
app.include_router(mascotas_router)
app.include_router(practicas_router)
app.include_router(turnos_router)
