from fastapi import APIRouter, HTTPException
from schemas.alquiler_schema import AlquilerCreate, AlquilerResponse
from services.alquiler_service import AlquilerService
from schemas.reserva_schema import ReservaAPI
from services.reserva_service import ReservaService




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


@router.post("/reserva", response_model=AlquilerResponse, tags=["Operaciones"])
def api_create_alquiler_from_reserva(rsrv: ReservaAPI):
    """
    Convierte una reserva en un alquiler.
    Verifica disponibilidad y actualiza el estado del vehículo a 'alquilado'.
    """
    ReservaService.reservaToAlquiler(rsrv.id_reserva, rsrv.id_empleado)