from pydantic import BaseModel, ConfigDict

class DetalleFacturaBase(BaseModel):
    id_detalle: int
    id_factura: int
    monto: float
    descripcion: str

class DetalleFacturaCreate(DetalleFacturaBase):
    pass

class DetalleFacturaResponse(DetalleFacturaBase):
    model_config = ConfigDict(from_attributes=True)
