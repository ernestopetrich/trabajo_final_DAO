from fastapi import APIRouter, HTTPException
from schemas.alquiler_schema import AlquilerCreate, AlquilerResponse, AlquilerCreateResponse
from services.alquiler_service import AlquilerService
from services.factura_service import FacturaService
from services.vehiculo_service import VehiculoService
from services.detalle_factura_service import DetalleFacturaService

router = APIRouter(prefix="/alquileres", tags=["Alquileres"])

@router.post("/", response_model=AlquilerCreateResponse)
def create_alquiler(data: AlquilerCreate):
    alq = AlquilerService.create(data.model_dump())
    if not alq:
        raise HTTPException(400, "No se pudo crear el alquiler")
    return alq
    

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
    print("Iniciando devolución del alquiler...")
    alq = AlquilerService.devolver(id_alquiler)
    if not alq:
        raise HTTPException(400, "No se pudo devolver el alquiler")
    
    return alq

@router.post("/{id_alquiler}/confirmar", response_model=AlquilerResponse)
def confirmar_alquiler(id_alquiler: int):
    alquiler = AlquilerService.confirmar(id_alquiler)
    if not alquiler:
        raise HTTPException(404, "Alquiler no encontrado")
    
    return alquiler

@router.post("/{id_alquiler}/iniciar", response_model=AlquilerResponse)
def iniciar_alquiler(id_alquiler: int):
    alquiler = AlquilerService.get_by_id(id_alquiler)
    if not alquiler:
        raise HTTPException(404, "Alquiler no encontrado")
    
    try:
        print("Iniciando el alquiler...")
        mensaje = alquiler.iniciar()
        alquiler_actualizado = AlquilerService.get_by_id(id_alquiler)
        return alquiler_actualizado
    except ValueError as ve:
        raise HTTPException(400, str(ve))


@router.post("/{id_alquiler}/delete")
def delete_alquiler(id_alquiler: int):
    success = AlquilerService.delete(id_alquiler)
    if not success:
        raise HTTPException(404, "Alquiler no encontrado o no se pudo dar de baja")
    return {"detail": "Alquiler {id_alquiler} dado de baja exitosamente"}

@router.put("/{id_alquiler}", response_model=AlquilerResponse)
def update_alquiler(id_alquiler: int, data: dict):
    actualizado = AlquilerService.update(id_alquiler, data)
    if not actualizado:
        raise HTTPException(400, "No se pudo actualizar el alquiler")
    return actualizado
