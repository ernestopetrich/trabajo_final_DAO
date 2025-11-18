from fastapi import APIRouter, HTTPException
from schemas.alquiler_schema import AlquilerCreate, AlquilerResponse
from services.alquiler_service import AlquilerService
from services.factura_service import FacturaService
from services.vehiculo_service import VehiculoService
from services.detalle_factura_service import DetalleFacturaService




router = APIRouter(prefix="/alquileres", tags=["Alquileres"])

@router.post("/", response_model=AlquilerResponse)
def create_alquiler(data: AlquilerCreate):
    alq = AlquilerService.create(data.dict())
    if not alq:
        raise HTTPException(400, "No se pudo crear el alquiler")
    else:
        # Aquí podrías agregar lógica para crear una factura asociada al alquiler
        factura_data = {
            "id_alquiler": alq.id_alquiler,
            "monto_total": alq.calcular_monto(),  # Suponiendo que existe este método
            "fecha_hora_emision": alq.fecha_hora_inicio
        }
        fac = FacturaService.create(factura_data)
        if not fac:
            raise HTTPException(400, "No se pudo crear la factura asociada")
        else:
            # Crear detalle de factura
            print("Creando detalle de factura...")
            DetalleFacturaService.create({
                "id_factura": fac.id_factura,
                "descripcion": f"Alquiler vehículo ID {alq.id_vehiculo}",
                "monto": fac.monto_total
            })
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
    devuelto = AlquilerService.devolver(id_alquiler)
    if not devuelto:
        raise HTTPException(400, "No se pudo devolver el alquiler")
    else:
        # Aquí podrías agregar lógica para actualizar la factura asociada al alquiler
        factura = FacturaService.get_by_alquiler(id_alquiler)
        if factura:
            VehiculoService.update(devuelto.id_vehiculo, {"estado": "disponible"})
            factura.estado_pago = "pagado"
            FacturaService.update(factura.id_factura, {"estado_pago": "pagado"})
    return devuelto