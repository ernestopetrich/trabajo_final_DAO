from fastapi import APIRouter
from schemas.multa_schema import MultaCreate, MultaResponse
from services.multa_service import MultaService

router = APIRouter(prefix="/multas", tags=["Multas"])

@router.post("/", response_model=MultaResponse)
def create_multa(data: MultaCreate):
    return MultaService.create(data.dict())

@router.get("/", response_model=list[MultaResponse])
def get_multas():
    return MultaService.get_all()

@router.get("/alquiler/{id_alquiler}", response_model=list[MultaResponse])
def get_multas_por_alquiler(id_alquiler: int):
    return MultaService.get_by_id_alquiler(id_alquiler)
