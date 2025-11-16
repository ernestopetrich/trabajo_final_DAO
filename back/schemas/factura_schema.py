from pydantic import BaseModel

class FacturaBase(BaseModel):
    id_alquiler: int
    fecha_hora_emision: str
    monto_total: float

class FacturaCreate(FacturaBase):
    pass

class FacturaResponse(FacturaBase):
    id_factura: int
    estado_pago: str
