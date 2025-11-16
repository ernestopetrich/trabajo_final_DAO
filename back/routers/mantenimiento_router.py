from fastapi import APIRouter, HTTPException
from schemas.mantenimiento_schema import MantenimientoCreate, MantenimientoUpdate, MantenimientoResponse
from services.mantenimiento_service import MantenimientoService

router = APIRouter(prefix="/mantenimientos", tags=["Mantenimientos"])

@router.post("/", response_model=MantenimientoResponse)
def create_mantenimiento(data: MantenimientoCreate):
    return MantenimientoService.create(data.dict())

@router.get("/", response_model=list[MantenimientoResponse])
def get_mantenimientos():
    return MantenimientoService.get_all()

@router.get("/{id_mantenimiento}", response_model=MantenimientoResponse)
def get_mantenimiento(id_mantenimiento: int):
    mant = MantenimientoService.get_by_id(id_mantenimiento)
    if not mant:
        raise HTTPException(404, "Mantenimiento no encontrado")
    return mant
