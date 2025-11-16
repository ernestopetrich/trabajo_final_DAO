from pydantic import BaseModel

class ReservaBase(BaseModel):
    id_cliente: int
    id_vehiculo: int
    fecha_inicio: str
    fecha_fin: str

class ReservaCreate(ReservaBase):
    pass

class ReservaEstadoUpdate(BaseModel):
    estado: str

class ReservaResponse(ReservaBase):
    id_reserva: int
    estado: str
