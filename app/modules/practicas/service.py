from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.errores import rechazo
from app.modules.practicas.models import Practica
from app.modules.practicas.schemas import PracticaCreate


async def crear_practica(session: AsyncSession, datos: PracticaCreate) -> Practica:
    practica = Practica(**datos.model_dump())
    session.add(practica)
    try:
        await session.commit()
        return practica
    except IntegrityError as error:
        await session.rollback()
        raise rechazo(
            "No se pudo crear la práctica: el nombre ya está registrado o el precio es inválido.",
            error,
        )


async def listar_practicas(session: AsyncSession) -> list[Practica]:
    consulta = select(Practica).order_by(Practica.id)
    return list((await session.exec(consulta)).all())
