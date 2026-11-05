import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[2] / ".env")

if "DATABASE_URL" not in os.environ:
    # Mejor una falla clara al arrancar que un error raro diez líneas más adelante.
    raise RuntimeError(
        "Falta la variable DATABASE_URL. Copiá env.example a .env "
        "(en la raíz del proyecto) y completá el valor."
    )

DATABASE_URL: str = os.environ["DATABASE_URL"]
