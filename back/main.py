import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import database
from datetime import datetime, timedelta

# IMPORTS DIRECTOS DE CADA ROUTER (forma más simple y segura)
from routers.cliente_router import router as cliente_router
from routers.empleado_router import router as empleado_router
from routers.vehiculo_router import router as vehiculo_router
from routers.alquiler_router import router as alquiler_router
from routers.mantenimiento_router import router as mantenimiento_router
from routers.multa_router import router as multa_router
from routers.danio_router import router as danio_router
from routers.factura_router import router as factura_router
from routers.reportes_router import router as reportes_router



# IMPORTS DIRECTOS DE MODELOS PARA CREAR DATOS DE EJEMPLO
from models.cliente import Cliente as ClienteModel
from models.vehiculo import Vehiculo as VehiculoModel
from models.alquiler import Alquiler as AlquilerModel
from models.empleado import Empleado as EmpleadoModel
from models.multa import Multa as MultaModel
from models.danio import Danio as DanioModel
from models.factura import Factura as FacturaModel
from models.detalle_factura import DetalleFactura as DetalleFacturaModel




app = FastAPI(
    title="API de AlquilaYa",
    description="API para la gestión de alquiler de vehículos.",
    version="1.0.0"
)

# --- CORS ---
origins = [
    "http://localhost:5175",
    "http://127.0.0.1:5175",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
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
        EmpleadoModel.create("DNI", "27555333", "Lucia", "Martinez")
        EmpleadoModel.create("DNI", "30444777", "Federico", "Ruiz")
        EmpleadoModel.create("DNI", "26322111", "Valentina", "Sosa")

        # Crear vehículos de ejemplo
        VehiculoModel.create("AA123BB", "Ford", "2018", "Fiesta", 15000.0)
        VehiculoModel.create("AC456DD", "Toyota", "2024", "Corolla", 22000.0)
        VehiculoModel.create("AE789FF", "VW", "2023", "Amarok", 35000.0)
        
        # Crear alquileres de ejemplo con distintos estados
        # ============================================================
        # 1) JUNIO — FINALIZADO — con multa
        # ============================================================
        junio = datetime(2024, 6, 10, 9, 0, 0)

        alq_junio = AlquilerModel.create_raw(
            id_cliente=1,
            id_vehiculo=1,
            id_empleado=1,
            fecha_inicio=junio.isoformat(timespec='seconds'),
            fecha_fin_prevista=(junio + timedelta(days=2)).isoformat(timespec='seconds'),
            fecha_fin_real=(junio + timedelta(days=2, hours=2)).isoformat(timespec='seconds'),
            estado="finalizado"
        )

        if alq_junio:
            MultaModel.create(
                id_alquiler=alq_junio.id_alquiler,
                descripcion="Estacionar en lugar prohibido",
                monto=22000,
                fecha_hora_multa=(junio + timedelta(days=1, hours=3)).isoformat(timespec='seconds')
            )

        if alq_junio:
            fac = FacturaModel.create(
                id_alquiler=alq_junio.id_alquiler,
                fecha_hora_emision=junio.isoformat(timespec="seconds"),
                monto_total=alq_junio.costo_total or 30000
            )

            if fac:
                DetalleFacturaModel.create(
                    id_factura=fac.id_factura,
                    descripcion=f"Alquiler vehículo {alq_junio.id_vehiculo}",
                    monto=fac.monto_total
                )

        # ============================================================
        # 2) JULIO — ACTIVO — sin multa ni daño
        # ============================================================
        julio = datetime(2024, 7, 5, 14, 0, 0)

        AlquilerModel.create_raw(
            id_cliente=2,
            id_vehiculo=2,
            id_empleado=1,
            fecha_inicio=julio.isoformat(timespec='seconds'),
            fecha_fin_prevista=(julio + timedelta(days=3)).isoformat(timespec='seconds'),
            estado="activo"
        )

        # ============================================================
        # 3) SEPTIEMBRE — FINALIZADO — con daño
        # ============================================================
        sept1 = datetime(2024, 9, 1, 11, 0, 0)

        alq_sep1 = AlquilerModel.create_raw(
            id_cliente=1,
            id_vehiculo=3,
            id_empleado=1,
            fecha_inicio=sept1.isoformat(timespec='seconds'),
            fecha_fin_prevista=(sept1 + timedelta(days=1)).isoformat(timespec='seconds'),
            fecha_fin_real=(sept1 + timedelta(days=1)).isoformat(timespec='seconds'),
            estado="finalizado"
        )

        if alq_sep1:
            DanioModel.create(
                id_alquiler=alq_sep1.id_alquiler,
                descripcion="Rotura en espejo lateral",
                costo_reparacion=30000,
                fecha_hora_reporte=(sept1 + timedelta(days=1, hours=1)).isoformat(timespec='seconds')
            )
        
        if alq_sep1:
            fac = FacturaModel.create(
                id_alquiler=alq_sep1.id_alquiler,
                fecha_hora_emision=sept1.isoformat(timespec="seconds"),
                monto_total=alq_sep1.costo_total or 55000
            )
            if fac:
                DetalleFacturaModel.create(
                    id_factura=fac.id_factura,
                    descripcion="Alquiler con daño",
                    monto=fac.monto_total
                )


        # ============================================================
        # 4) SEPTIEMBRE (otro) — PENDIENTE
        # ============================================================
        sept2 = datetime(2024, 9, 20, 10, 30, 0)

        AlquilerModel.create_raw(
            id_cliente=2,
            id_vehiculo=1,
            id_empleado=1,
            fecha_inicio=sept2.isoformat(timespec='seconds'),
            fecha_fin_prevista=(sept2 + timedelta(days=2)).isoformat(timespec='seconds'),
            estado="pendiente"
        )

        # ============================================================
        # 5) OCTUBRE — CONFIRMADO — reserva lista para retirar
        # ============================================================
        octu = datetime(2024, 10, 12, 8, 0, 0)

        AlquilerModel.create_raw(
            id_cliente=1,
            id_vehiculo=2,
            id_empleado=1,
            fecha_inicio=octu.isoformat(timespec='seconds'),
            fecha_fin_prevista=(octu + timedelta(days=3)).isoformat(timespec='seconds'),
            estado="confirmado"
        )

        print("Alquileres de ejemplo generados correctamente.")

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
app.include_router(reportes_router)




# --- RUN SERVER ---
if __name__ == "__main__":
    setup_database()
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
