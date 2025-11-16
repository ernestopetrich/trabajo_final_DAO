from pydantic import BaseModel

class VehiculoBase(BaseModel):
    patente: str
    marca: str
    modelo: str
    nombre: str | None = None
    precio_diario: float

class VehiculoCreate(VehiculoBase):
    pass

class VehiculoUpdate(BaseModel):
    patente: str | None = None
    marca: str | None = None
    modelo: str | None = None
    nombre: str | None = None
    precio_diario: float | None = None

class VehiculoEstadoUpdate(BaseModel):
    estado: str

class VehiculoResponse(VehiculoBase):
    id_vehiculo: int
    estado: str
