from fastapi import APIRouter
from schemas.danio_schema import DanioCreate, DanioResponse
from services.danio_service import DanioService

router = APIRouter(prefix="/danios", tags=["Daños"])

@router.post("/", response_model=DanioResponse)
def create_danio(data: DanioCreate):
    return DanioService.create(data.dict())

@router.get("/", response_model=list[DanioResponse])
def get_danios():
    return DanioService.get_all()

@router.get("/alquiler/{id_alquiler}", response_model=list[DanioResponse])
def get_danios_por_alquiler(id_alquiler: int):
    return DanioService.get_by_id_alquiler(id_alquiler)
