from pydantic import BaseModel

class MantenimientoBase(BaseModel):
    id_vehiculo: int
    fecha_hora_inicio: str
    fecha_hora_fin: str | None = None
    descripcion: str
    costo: float | None = None

class MantenimientoCreate(MantenimientoBase):
    pass

class MantenimientoUpdate(BaseModel):
    fecha_hora_inicio: str | None = None
    fecha_hora_fin: str | None = None
    descripcion: str | None = None
    costo: float | None = None

class MantenimientoResponse(MantenimientoBase):
    id_mantenimiento: int
