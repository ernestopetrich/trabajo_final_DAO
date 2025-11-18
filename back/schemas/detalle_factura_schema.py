from pydantic import BaseModel

class DetalleFacturaBase(BaseModel):
    id_detalle: int
    id_factura: int
    monto: float
    descripcion: str

class DetalleFacturaCreate(FacturaBase):
    pass

class DetalleFacturaResponse(FacturaBase):
    id_factura: int
    id_detalle: int
    monto: float
    descripcion: str
