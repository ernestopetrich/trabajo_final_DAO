from fastapi import APIRouter, HTTPException
from schemas.alquiler_schema import AlquilerCreate, AlquilerResponse
from services.alquiler_service import AlquilerService

router = APIRouter(prefix="/alquileres", tags=["Alquileres"])

@router.post("/", response_model=AlquilerResponse)
def create_alquiler(data: AlquilerCreate):
    return AlquilerService.create(data.dict())

@router.get("/", response_model=list[AlquilerResponse])
def get_alquileres():
    return AlquilerService.get_all()

@router.get("/{id_alquiler}", response_model=AlquilerResponse)
def get_alquiler(id_alquiler: int):
    alquiler = AlquilerService.get_by_id(id_alquiler)
    if not alquiler:
        raise HTTPException(404, "Alquiler no encontrado")
    return alquiler

@router.post("/{id_alquiler}/devolver", response_model=AlquilerResponse)
def devolver_alquiler(id_alquiler: int):
    devuelto = AlquilerService.devolver(id_alquiler)
    if not devuelto:
        raise HTTPException(400, "No se pudo devolver el alquiler")
    return devuelto
