from fastapi import APIRouter
from schemas.factura_schema import FacturaCreate, FacturaResponse
from services.factura_service import FacturaService

router = APIRouter(prefix="/facturas", tags=["Facturas"])

@router.post("/", response_model=FacturaResponse)
def create_factura(data: FacturaCreate):
    return FacturaService.create(data.dict())

@router.get("/", response_model=list[FacturaResponse])
def get_facturas():
    return FacturaService.get_all()

@router.get("/{id_factura}", response_model=FacturaResponse)
def get_factura(id_factura: int):
    return FacturaService.get_by_id(id_factura)
