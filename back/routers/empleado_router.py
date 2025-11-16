from fastapi import APIRouter
from schemas.empleado_schema import EmpleadoCreate, EmpleadoResponse
from services.empleado_service import EmpleadoService

router = APIRouter(prefix="/empleados", tags=["Empleados"])

@router.post("/", response_model=EmpleadoResponse)
def create_empleado(data: EmpleadoCreate):
    return EmpleadoService.create(data.dict())

@router.get("/", response_model=list[EmpleadoResponse])
def get_empleados():
    return EmpleadoService.get_all()

@router.get("/{id_empleado}", response_model=EmpleadoResponse)
def get_empleado(id_empleado: int):
    return EmpleadoService.get_by_id(id_empleado)
