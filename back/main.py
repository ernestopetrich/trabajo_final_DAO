import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict
from typing import List
import database
# Importamos los modelos de la lógica de BD con un alias "Model"
# para evitar colisiones de nombres con los modelos Pydantic.
from models import (
    Vehiculo as VehiculoModel, 
    Cliente as ClienteModel, 
    Reserva as ReservaModel, 
    Alquiler as AlquilerModel, 
    Empleado as EmpleadoModel,
    Mantenimiento as MantenimientoModel
)
import os
from datetime import datetime, timedelta

# --- Schemas (Modelos Pydantic para validación de API) ---
# Estos modelos definen cómo se ven los datos al entrar y salir de la API.

class ClienteBase(BaseModel):
    tipo_dni: str
    dni: str
    nombre: str
    apellido: str
    telefono: str | None = None
    email: str | None = None
    direccion: str | None = None

class ClienteCreate(ClienteBase):
    pass # Se usa para crear, no necesita ID

class Cliente(ClienteBase):
    id_cliente: int
    model_config = ConfigDict(from_attributes=True)

class EmpleadoBase(BaseModel):
    tipo_dni: str
    dni: str
    nombre: str
    apellido: str

class EmpleadoCreate(EmpleadoBase):
    pass

class Empleado(EmpleadoBase):
    id_empleado: int
    model_config = ConfigDict(from_attributes=True)

class VehiculoBase(BaseModel):
    patente: str
    marca: str
    modelo: str
    nombre: str | None = None
    precio_diario: float

class VehiculoCreate(VehiculoBase):
    pass

class Vehiculo(VehiculoBase):
    id_vehiculo: int
    estado: str
    model_config = ConfigDict(from_attributes=True)

class ReservaBase(BaseModel):
    id_cliente: int
    id_vehiculo: int
    fecha_inicio: str # Usamos str para fechas por simplicidad (ej. "YYYY-MM-DD HH:MM:SS")
    fecha_fin: str

class ReservaCreate(ReservaBase):
    pass

class ReservaAPI(ReservaBase):
    id_reserva: int
    id_empleado: int | None = None

class Reserva(ReservaBase):
    id_reserva: int
    estado: str
    model_config = ConfigDict(from_attributes=True)

class AlquilerBase(BaseModel):
    id_cliente: int
    id_vehiculo: int
    id_empleado: int
    fecha_hora_inicio: str
    fecha_hora_fin_prevista: str

class AlquilerCreate(AlquilerBase):
    pass

class Alquiler(AlquilerBase):
    id_alquiler: int
    fecha_hora_fin_real: str | None = None
    costo_total: float | None = None
    estado: str
    model_config = ConfigDict(from_attributes=True)


# --- Configuración de la Aplicación ---

app = FastAPI(
    title="API de AlquilaYa",
    description="API para la gestión de alquiler de vehículos.",
    version="1.0.0"
)

def setup_database():
    """Inicializa la base de datos y crea datos de ejemplo si es nueva."""
    is_new_db = not os.path.exists(database.DATABASE_FILE)
    database.create_tables()
    
    if is_new_db:
        print("Base de datos nueva. Creando datos de ejemplo...")
        
        # Usamos los alias ...Model para llamar a los métodos de clase
        
        # Crear clientes de ejemplo
        ClienteModel.create("DNI", "30123456", "Juan", "Perez", "1155443322", "juan@email.com", "Av. Siempre Viva 123")
        ClienteModel.create("DNI", "35654321", "Maria", "Gomez", "1122334455", "maria@email.com", "Calle Falsa 456")
        
        # Crear empleado de ejemplo
        EmpleadoModel.create("DNI", "28999111", "Carlos", "Lopez")

        # Crear vehículos de ejemplo
        VehiculoModel.create("AA123BB", "Ford", "Fiesta", "Compacto", 15000.0)
        VehiculoModel.create("AC456DD", "Toyota", "Corolla", "Sedan", 22000.0)
        VehiculoModel.create("AE789FF", "VW", "Amarok", "Camioneta", 35000.0)
        print("Datos de ejemplo creados.")


# --- Endpoints de la API ---


# Clients Endpoints
@app.post("/clientes/", response_model=Cliente, tags=["Clientes"])
def api_create_cliente(cliente: ClienteCreate):
    """Crea un nuevo cliente."""
    
    db_cliente = ClienteModel.get_by_dni(cliente.dni)
    if db_cliente:
        raise HTTPException(status_code=400, detail="El DNI ya está registrado")
    
    nuevo_cliente = ClienteModel.create(**cliente.model_dump())
    if not nuevo_cliente:
        raise HTTPException(status_code=500, detail="Error al crear el cliente")
    return nuevo_cliente

@app.get("/clientes/{cliente_id}", response_model=Cliente, tags=["Clientes"])
def api_get_cliente_by_id(cliente_id: int):
    """Obtiene un cliente por su ID."""
    cliente = ClienteModel.get_by_id(cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente



# Vehículos Endpoints
@app.post("/vehiculos/", response_model=Vehiculo, tags=["Vehículos"])
def api_create_vehiculo(vehiculo: VehiculoCreate):
    """Crea un nuevo vehículo."""
    nuevo_vehiculo = VehiculoModel.create(**vehiculo.model_dump())
    if not nuevo_vehiculo:
        raise HTTPException(status_code=400, detail="Error al crear el vehículo (¿patente duplicada?)")
    return nuevo_vehiculo

@app.get("/vehiculos/{vehiculo_id}", response_model=Vehiculo, tags=["Vehículos"])
def api_get_vehiculo_by_id(vehiculo_id: int):
    """Obtiene un vehículo por su ID."""
    vehiculo = VehiculoModel.get_by_id(vehiculo_id)
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return vehiculo

@app.get("/vehiculos/", response_model=List[Vehiculo], tags=["Vehículos"])
def api_list_vehiculos():
    """Lista todos los vehículos."""
    
    vehiculos = VehiculoModel.get_all()
    return vehiculos


# Empleados Endpoints
@app.get("/empleados/", response_model=List[Empleado], tags=["Empleados"])
def api_list_empleados():
    """Lista todos los empleados."""
    empleados = EmpleadoModel.get_all()
    return empleados

# Reservas Endpoints
@app.post("/reservas/", response_model=Reserva, tags=["Operaciones"])
def api_create_reserva(reserva: ReservaCreate):
    """
    Crea una nueva reserva anticipada.
    Verifica la disponibilidad del vehículo antes de confirmar.
    """
    # Validar que existen los objetos
    cliente = ClienteModel.get_by_id(reserva.id_cliente)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    vehiculo = VehiculoModel.get_by_id(reserva.id_vehiculo)
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")

    # Verificar disponibilidad
    if not vehiculo.is_available(reserva.fecha_inicio, reserva.fecha_fin):
        raise HTTPException(status_code=400, detail="Vehículo no disponible en las fechas solicitadas")

    # Crear la reserva
    nueva_reserva = ReservaModel.create(
        id_cliente=reserva.id_cliente,
        id_vehiculo=reserva.id_vehiculo,
        fecha_inicio=reserva.fecha_inicio,
        fecha_fin=reserva.fecha_fin,
        estado='confirmada' # O 'pendiente' si requiere aprobación
    )
    if not nueva_reserva:
        raise HTTPException(status_code=500, detail="Error al guardar la reserva")
    
    return nueva_reserva

@app.get("/reservas/", response_model=List[Reserva], tags=["Operaciones"])
def api_list_reservas():
    """Lista todas las reservas."""
    reservas = ReservaModel.get_all()
    return reservas


# Alquileres Endpoints
@app.post("/alquileres/", response_model=Alquiler, tags=["Operaciones"])
def api_create_alquiler(alquiler: AlquilerCreate):
    """
    Crea un nuevo alquiler (directo).
    Verifica disponibilidad y actualiza el estado del vehículo a 'alquilado'.
    """
    # Validar que existen los objetos
    cliente = ClienteModel.get_by_id(alquiler.id_cliente)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    vehiculo = VehiculoModel.get_by_id(alquiler.id_vehiculo)
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    
    empleado = EmpleadoModel.get_by_id(alquiler.id_empleado)
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

    # Lógica de negocio: Verificar disponibilidad
    if not vehiculo.is_available(alquiler.fecha_hora_inicio, alquiler.fecha_hora_fin_prevista):
        raise HTTPException(status_code=400, detail="Vehículo no disponible en este momento")

    # Crear el alquiler (el modelo se encarga de actualizar el estado del vehiculo)
    nuevo_alquiler = AlquilerModel.create(
        id_cliente=alquiler.id_cliente,
        id_vehiculo=alquiler.id_vehiculo,
        id_empleado=alquiler.id_empleado,
        fecha_hora_inicio=alquiler.fecha_hora_inicio,
        fecha_hora_fin_prevista=alquiler.fecha_hora_fin_prevista
    )
    
    if not nuevo_alquiler:
        raise HTTPException(status_code=500, detail="Error al crear el alquiler")

    return nuevo_alquiler

@app.post("/alquileres/reserva/", response_model=Alquiler, tags=["Operaciones"])
def api_create_alquiler_from_reserva(rsrv: ReservaAPI):
    print(rsrv)
    """
    Convierte una reserva en un alquiler.
    Verifica disponibilidad y actualiza el estado del vehículo a 'alquilado'.
    """


    reserva = ReservaModel.get_by_id(rsrv.id_reserva)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    
    if reserva.fecha_inicio < datetime.now().strftime("%d/%m/%Y"):
        raise HTTPException(status_code=400, detail="La fecha de inicio de la reserva ya pasó")
    
    elif reserva.fecha_inicio > (datetime.now() + timedelta(days=2)).strftime("%d/%m/%Y"):
        raise HTTPException(status_code=400, detail="Solo se pueden convertir reservas con hasta 2 días de anticipación")

    if reserva.estado != 'confirmada':
        raise HTTPException(status_code=400, detail="Solo se pueden convertir reservas confirmadas")

    vehiculo = VehiculoModel.get_by_id(reserva.id_vehiculo)
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")

    empleado = EmpleadoModel.get_by_id(rsrv.id_empleado)
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

    # Verificar disponibilidad
    if not vehiculo.is_available(reserva.fecha_inicio, reserva.fecha_fin):
        raise HTTPException(status_code=400, detail="Vehículo no disponible en este momento")

    # Crear el alquiler
    nuevo_alquiler = AlquilerModel.create(
        id_cliente=reserva.id_cliente,
        id_vehiculo=reserva.id_vehiculo,
        id_empleado=id_empleado,
        fecha_hora_inicio=reserva.fecha_inicio,
        fecha_hora_fin_prevista=reserva.fecha_fin
    )
    
    if not nuevo_alquiler:
        raise HTTPException(status_code=500, detail="Error al crear el alquiler desde la reserva")

    # Actualizar estado de la reserva
    reserva.update_estado('convertida')

    return nuevo_alquiler


if __name__ == "__main__":
    setup_database() # Prepara la BD y datos de ejemplo
    print("Iniciando API server en http://127.0.0.1:8000")
    print("Accede a la documentación interactiva en http://127.0.0.1:8000/docs")
    
    # Uvicorn corre la app. "main:app" le dice que busque el objeto "app" en el archivo "main.py".
    # reload=True hace que el servidor se reinicie automáticamente cuando guardas cambios en el código.
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)