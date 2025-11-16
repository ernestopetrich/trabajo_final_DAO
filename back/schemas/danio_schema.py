from pydantic import BaseModel

class DanioBase(BaseModel):
    id_alquiler: int
    descripcion: str
    costo_reparacion: float
    fecha_hora_reporte: str

class DanioCreate(DanioBase):
    pass

class DanioResponse(DanioBase):
    id_danio: int
    estado: str
