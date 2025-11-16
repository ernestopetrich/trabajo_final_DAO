from pydantic import BaseModel

class EmpleadoBase(BaseModel):
    tipo_dni: str
    dni: str
    nombre: str
    apellido: str

class EmpleadoCreate(EmpleadoBase):
    pass

class EmpleadoResponse(EmpleadoBase):
    id_empleado: int
