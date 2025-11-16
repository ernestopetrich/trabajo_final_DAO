from pydantic import BaseModel

class ClienteBase(BaseModel):
    tipo_dni: str
    dni: str
    nombre: str
    apellido: str
    telefono: str | None = None
    email: str | None = None
    direccion: str | None = None

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(BaseModel):
    tipo_dni: str | None = None
    dni: str | None = None
    nombre: str | None = None
    apellido: str | None = None
    telefono: str | None = None
    email: str | None = None
    direccion: str | None = None

class ClienteResponse(ClienteBase):
    id_cliente: int
