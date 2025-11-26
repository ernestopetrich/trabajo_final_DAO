from fastapi import APIRouter, HTTPException
from schemas.cliente_schema import ClienteCreate, ClienteUpdate, ClienteResponse
from services.cliente_service import ClienteService

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.post("/", response_model=ClienteResponse)
def create_cliente(data: ClienteCreate):
    return ClienteService.create(data.model_dump())

@router.get("/", response_model=list[ClienteResponse])
def get_clientes():
    return ClienteService.get_all()

@router.get("/{id_cliente}", response_model=ClienteResponse)
def get_cliente(id_cliente: int):
    cliente = ClienteService.get_by_id(id_cliente)
    if not cliente:
        raise HTTPException(404, "Cliente no encontrado")
    return cliente

@router.put("/{id_cliente}", response_model=ClienteResponse)
def update_cliente(id_cliente: int, data: ClienteUpdate):
    actualizado = ClienteService.update(id_cliente, data.dict())
    if not actualizado:
        raise HTTPException(400, "Error al actualizar cliente")
    return actualizado

@router.put("/{id_cliente}/delete")
def delete_cliente(id_cliente: int):
    eliminado = ClienteService.delete(id_cliente)
    if not eliminado:
        raise HTTPException(400, "Error al dar de baja el cliente")
    return {"detail": "Cliente dado de baja exitosamente"}
