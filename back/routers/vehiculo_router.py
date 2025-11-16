from fastapi import APIRouter, HTTPException
from schemas.vehiculo_schema import VehiculoCreate, VehiculoUpdate, VehiculoResponse
from services.vehiculo_service import VehiculoService

router = APIRouter(prefix="/vehiculos", tags=["Vehículos"])

@router.post("/", response_model=VehiculoResponse)
def create_vehiculo(data: VehiculoCreate):
    return VehiculoService.create(data.dict())

@router.get("/", response_model=list[VehiculoResponse])
def get_all():
    return VehiculoService.get_all()

@router.get("/{id_vehiculo}", response_model=VehiculoResponse)
def get_vehiculo(id_vehiculo: int):
    veh = VehiculoService.get_by_id(id_vehiculo)
    if not veh:
        raise HTTPException(404, "Vehículo no encontrado")
    return veh

@router.put("/{id_vehiculo}", response_model=VehiculoResponse)
def update_vehiculo(id_vehiculo: int, data: VehiculoUpdate):
    actualizado = VehiculoService.update(id_vehiculo, data.dict())
    if not actualizado:
        raise HTTPException(400, "No se pudo actualizar")
    return actualizado

@router.delete("/{id_vehiculo}")
def delete(id_vehiculo: int):
    eliminado = VehiculoService.delete(id_vehiculo)
    if not eliminado:
        raise HTTPException(400, "No se pudo eliminar")
    return {"detail": "Vehículo eliminado"}
