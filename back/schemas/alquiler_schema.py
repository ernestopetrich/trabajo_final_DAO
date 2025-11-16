from pydantic import BaseModel

class AlquilerBase(BaseModel):
    id_cliente: int
    id_vehiculo: int
    id_empleado: int
    fecha_hora_inicio: str
    fecha_hora_fin_prevista: str

class AlquilerCreate(AlquilerBase):
    pass

class AlquilerResponse(AlquilerBase):
    id_alquiler: int
    fecha_hora_fin_real: str | None = None
    costo_total: float | None = None
    estado: str
