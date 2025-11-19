import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import database

# IMPORTS DIRECTOS DE CADA ROUTER (forma más simple y segura)
from routers.cliente_router import router as cliente_router
from routers.empleado_router import router as empleado_router
from routers.vehiculo_router import router as vehiculo_router
from routers.alquiler_router import router as alquiler_router
from routers.mantenimiento_router import router as mantenimiento_router
from routers.multa_router import router as multa_router
from routers.danio_router import router as danio_router
from routers.factura_router import router as factura_router


# IMPORTS DIRECTOS DE MODELOS PARA CREAR DATOS DE EJEMPLO
from models.cliente import Cliente as ClienteModel
from models.vehiculo import Vehiculo as VehiculoModel
from models.alquiler import Alquiler as AlquilerModel
from models.empleado import Empleado as EmpleadoModel




app = FastAPI(
    title="API de AlquilaYa",
    description="API para la gestión de alquiler de vehículos.",
    version="1.0.0"
)

# --- CORS ---
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- DATABASE INIT ---
def setup_database():
    is_new_db = not os.path.exists(database.DATABASE_FILE)
    print("USANDO BD:", os.path.abspath(database.DATABASE_FILE))
    database.create_tables()

    if is_new_db:
        print("Base de datos creada por primera vez. Agregando datos de ejemplo...")

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


# --- RUTA PRINCIPAL ---
@app.get("/", tags=["General"])
def root():
    return "API AlquilaYa funcionando correctamente."


# --- INCLUIR TODOS LOS ROUTERS ---
app.include_router(cliente_router)
app.include_router(empleado_router)
app.include_router(vehiculo_router)
app.include_router(alquiler_router)
app.include_router(mantenimiento_router)
app.include_router(multa_router)
app.include_router(danio_router)
app.include_router(factura_router)


# --- RUN SERVER ---
if __name__ == "__main__":
    setup_database()
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)
