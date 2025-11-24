from pydantic import BaseModel, ConfigDict
from schemas.cliente_schema import ClienteResponse
from schemas.detalle_factura_schema import DetalleFacturaResponse

class FacturaBase(BaseModel):
    id_alquiler: int
    fecha_hora_emision: str
    monto_total: float
    


class FacturaCreate(FacturaBase):
    pass

class FacturaResponse(FacturaBase):
    id_factura: int


class FacturaResponseAlquiler(FacturaBase):
    id_factura: int
    cliente: ClienteResponse
    items: list[DetalleFacturaResponse]
    subtotal: float
    impuestos: float
    total: float
    model_config = ConfigDict(from_attributes=True)
