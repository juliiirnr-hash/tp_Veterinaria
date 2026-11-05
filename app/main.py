from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

import app.core.modelos
app = FastAPI(
    title="Capítulo 4 completo — persistencia: SQLModel, PostgreSQL y el modelo de datos",
    version="1.0.0",
    description=(
        "El proyecto que acompaña a la presentación del capítulo 4, diapositiva por diapositiva.\n\n"
        "**Parte 1 · cómo se guardan las relaciones** (diapositivas 3 a 8): clave foránea, uno a "
        "muchos, uno a uno, muchos a muchos con dato propio, agregación y composición, qué pasa al "
        "borrar y el índice de la clave foránea.\n\n"
        "**Parte 2 · cómo se leen** (diapositivas 10 a 15): `Relationship()` con `back_populates`, "
        "declarar no es cargar, el N+1, `selectinload`, la excepción `MissingGreenlet` y "
        "`joinedload`. Esas respuestas traen `consultas_emitidas`.\n\n"
        "**Parte 3 · el esquema en la práctica** (diapositivas 17 y 18): CHECK y unicidad en la "
        "base.\n\n"
        "Páginas para probarlo en vivo: [la página de inicio](/)."
    ),
    lifespan=lifespan,
)