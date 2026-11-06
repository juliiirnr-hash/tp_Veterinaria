from sqlmodel import SQLModel


class SaludLive(SQLModel):
    estado: str


class SaludReady(SQLModel):
    estado: str
