from fastapi import APIRouter, HTTPException
from schemas.reserva_schema import ReservaCreate, ReservaEstadoUpdate, ReservaResponse
from services.reserva_service import ReservaService

router = APIRouter(prefix="/reservas", tags=["Reservas"])

@router.post("/", response_model=ReservaResponse)
def create_reserva(data: ReservaCreate):
    return ReservaService.create(data.dict())

@router.get("/", response_model=list[ReservaResponse])
def get_reservas():
    return ReservaService.get_all()

@router.get("/{id_reserva}", response_model=ReservaResponse)
def get_reserva(id_reserva: int):
    reserva = ReservaService.get_by_id(id_reserva)
    if not reserva:
        raise HTTPException(404, "Reserva no encontrada")
    return reserva

@router.patch("/{id_reserva}/estado", response_model=ReservaResponse)
def update_estado(id_reserva: int, data: ReservaEstadoUpdate):
    actualizado = ReservaService.update_estado(id_reserva, data.estado)
    if not actualizado:
        raise HTTPException(400, "Error al actualizar estado")
    return actualizado
