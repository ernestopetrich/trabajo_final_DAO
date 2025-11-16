import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import database

# IMPORTS DIRECTOS DE CADA ROUTER (forma más simple y segura)
from routers.cliente_router import router as cliente_router
from routers.empleado_router import router as empleado_router
from routers.vehiculo_router import router as vehiculo_router
from routers.reserva_router import router as reserva_router
from routers.alquiler_router import router as alquiler_router
from routers.mantenimiento_router import router as mantenimiento_router
from routers.multa_router import router as multa_router
from routers.danio_router import router as danio_router
from routers.factura_router import router as factura_router


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
    database.create_tables()

    if is_new_db:
        print("Base de datos nueva. Sin datos de ejemplo cargados automáticamente.")
        # Si querés seeds, los agregamos luego.


# --- RUTA PRINCIPAL ---
@app.get("/", tags=["General"])
def root():
    return "API AlquilaYa funcionando correctamente."


# --- INCLUIR TODOS LOS ROUTERS ---
setup_database()
app.include_router(cliente_router)
app.include_router(empleado_router)
app.include_router(vehiculo_router)
app.include_router(reserva_router)
app.include_router(alquiler_router)
app.include_router(mantenimiento_router)
app.include_router(multa_router)
app.include_router(danio_router)
app.include_router(factura_router)


# --- RUN SERVER ---
if __name__ == "__main__":
    setup_database()
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
