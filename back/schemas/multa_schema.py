from pydantic import BaseModel

class MultaBase(BaseModel):
    id_alquiler: int
    descripcion: str
    monto: float
    fecha_hora_multa: str

class MultaCreate(MultaBase):
    pass

class MultaResponse(MultaBase):
    id_multa: int
    estado: str
