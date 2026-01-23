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
from services.vehiculo_service import VehiculoService
from services.multa_service import MultaService
from services.danio_service import DanioService
from services.factura_service import FacturaService
from services.detalle_factura_service import DetalleFacturaService




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
        
        # ============================================================
        # 1) JUNIO — FINALIZADO — con multa
        # ============================================================
        junio = datetime(2025, 6, 10, 9, 0, 0)

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
            # Crear multa
            MultaModel.create(
                id_alquiler=alq_junio.id_alquiler,
                descripcion="Estacionar en lugar prohibido",
                monto=22000,
                fecha_hora_multa=(junio + timedelta(days=1, hours=3)).isoformat(timespec='seconds')
            )

            # Calcular costo total (incluye alquiler + multa)
            costo = alq_junio.calcular_y_guardar_costo()
            cantidad_dias = alq_junio.calcular_dias_alquiler()
            
            vehiculo = VehiculoService.get_by_id(alq_junio.id_vehiculo)
            precio_diario = vehiculo.precio_diario
            
            # Crear factura
            fac = FacturaService.create({
                "id_alquiler": alq_junio.id_alquiler,
                "fecha_hora_emision": junio.isoformat(timespec='seconds'),
                "monto_total": costo,
                "estado_pago": "abonado"
            })

            if fac:
                # Detalle 1: Alquiler (precio unitario × cantidad de días)
                DetalleFacturaService.create({
                    "id_factura": fac.id_factura,
                    "descripcion": f"Alquiler vehículo {vehiculo.marca} {vehiculo.nombre} {vehiculo.modelo} ({vehiculo.patente})",
                    "cantidad": cantidad_dias,
                    "monto": precio_diario
                })
                
                # Detalle 2: Multa
                multas = MultaService.get_by_id_alquiler(alq_junio.id_alquiler)
                if multas:
                    for multa in multas:
                        DetalleFacturaService.create({
                            "id_factura": fac.id_factura,
                            "descripcion": f"Multa: {multa.descripcion}",
                            "cantidad": 1,
                            "monto": multa.monto
                        })

        # ============================================================
        # 2) Noviembre — ACTIVO
        # ============================================================
        noviembre = datetime(2025, 11, 15, 14, 0, 0)

        AlquilerModel.create_raw(
            id_cliente=2,
            id_vehiculo=2,
            id_empleado=1,
            fecha_inicio=noviembre.isoformat(timespec='seconds'),
            fecha_fin_prevista=(noviembre + timedelta(days=12)).isoformat(timespec='seconds'),
            estado="activo"
        )
        VehiculoService.update_estado(2, "alquilado")

        # ============================================================
        # 3) SEPTIEMBRE — FINALIZADO — con daño
        # ============================================================
        sept1 = datetime(2025, 9, 1, 11, 0, 0)

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
            # Crear daño
            DanioModel.create(
                id_alquiler=alq_sep1.id_alquiler,
                descripcion="Rotura en espejo lateral",
                costo_reparacion=20000,
                fecha_hora_reporte=(sept1 + timedelta(days=1, hours=1)).isoformat(timespec='seconds')
            )
            
            # Calcular costo total (incluye alquiler + daño)
            costo = alq_sep1.calcular_y_guardar_costo()
            cantidad_dias = alq_sep1.calcular_dias_alquiler()
            
            vehiculo = VehiculoService.get_by_id(alq_sep1.id_vehiculo)
            precio_diario = vehiculo.precio_diario
            
            # Crear factura
            fac = FacturaService.create({
                "id_alquiler": alq_sep1.id_alquiler,
                "fecha_hora_emision": sept1.isoformat(timespec='seconds'),
                "monto_total": costo,
                "estado_pago": "abonado"
            })
            
            if fac:
                # Detalle 1: Alquiler (precio unitario × cantidad de días)
                DetalleFacturaService.create({
                    "id_factura": fac.id_factura,
                    "descripcion": f"Alquiler vehículo {vehiculo.marca} {vehiculo.nombre} {vehiculo.modelo} ({vehiculo.patente})",
                    "cantidad": cantidad_dias,
                    "monto": precio_diario
                })
                
                # Detalle 2: Daño
                danios = DanioService.get_by_id_alquiler(alq_sep1.id_alquiler)
                if danios:
                    for danio in danios:
                        DetalleFacturaService.create({
                            "id_factura": fac.id_factura,
                            "descripcion": f"Daño: {danio.descripcion}",
                            "cantidad": 1,
                            "monto": danio.costo_reparacion
                        })


        # ============================================================
        # 4) SEPTIEMBRE — FINALIZADO — sin multa ni daño
        # ============================================================
        sept2 = datetime(2025, 9, 20, 10, 30, 0)

        alq_sept2 = AlquilerModel.create_raw(
            id_cliente=2,
            id_vehiculo=1,
            id_empleado=1,
            fecha_inicio=sept2.isoformat(timespec='seconds'),
            fecha_fin_prevista=(sept2 + timedelta(days=2)).isoformat(timespec='seconds'),
            fecha_fin_real=(sept2 + timedelta(days=2)).isoformat(timespec='seconds'),
            estado="finalizado"
        )

        if alq_sept2:
            # Calcular costo total (solo alquiler, sin multas/daños)
            costo = alq_sept2.calcular_y_guardar_costo()
            cantidad_dias = alq_sept2.calcular_dias_alquiler()
            
            vehiculo = VehiculoService.get_by_id(alq_sept2.id_vehiculo)
            precio_diario = vehiculo.precio_diario
            
            # Crear factura
            fac = FacturaService.create({
                "id_alquiler": alq_sept2.id_alquiler,
                "fecha_hora_emision": sept2.isoformat(timespec='seconds'),
                "monto_total": costo,
                "estado_pago": "abonado"
            })
            
            if fac:
                # Detalle: Alquiler (precio unitario × cantidad de días)
                DetalleFacturaService.create({
                    "id_factura": fac.id_factura,
                    "descripcion": f"Alquiler vehículo {vehiculo.marca} {vehiculo.nombre} {vehiculo.modelo} ({vehiculo.patente})",
                    "cantidad": cantidad_dias,
                    "monto": precio_diario
                })

        # ============================================================
        # 5) Noviembre — CONFIRMADO — reserva lista para retirar
        # ============================================================
        nov = datetime(2025, 11, 26, 8, 0, 0)

        AlquilerModel.create_raw(
            id_cliente=1,
            id_vehiculo=3,
            id_empleado=1,
            fecha_inicio=nov.isoformat(timespec='seconds'),
            fecha_fin_prevista=(nov + timedelta(days=3)).isoformat(timespec='seconds'),
            estado="confirmado"
        )

        # ============================================================
        # NUEVOS ALQUILERES SOLICITADOS
        # 1) SEPTIEMBRE — FINALIZADO — sin multa ni daño
        # ============================================================
        sept_extra = datetime(2025, 9, 10, 9, 0, 0)

        alq_sep_extra = AlquilerModel.create_raw(
            id_cliente=2,
            id_vehiculo=2,
            id_empleado=1,
            fecha_inicio=sept_extra.isoformat(timespec='seconds'),
            fecha_fin_prevista=(sept_extra + timedelta(days=2)).isoformat(timespec='seconds'),
            fecha_fin_real=(sept_extra + timedelta(days=2, hours=1)).isoformat(timespec='seconds'),
            estado="finalizado"
        )

        if alq_sep_extra:
            # Calcular costo total (sin multas/daños, solo alquiler)
            costo = alq_sep_extra.calcular_y_guardar_costo()
            cantidad_dias = alq_sep_extra.calcular_dias_alquiler()
            
            vehiculo = VehiculoService.get_by_id(alq_sep_extra.id_vehiculo)
            precio_diario = vehiculo.precio_diario
            
            # Crear factura
            fac = FacturaService.create({
                "id_alquiler": alq_sep_extra.id_alquiler,
                "fecha_hora_emision": sept_extra.isoformat(timespec='seconds'),
                "monto_total": costo,
                "estado_pago": "abonado"
            })
            
            if fac:
                # Detalle: precio unitario × cantidad de días
                DetalleFacturaService.create({
                    "id_factura": fac.id_factura,
                    "descripcion": f"Alquiler vehículo {vehiculo.marca} {vehiculo.nombre} {vehiculo.modelo} ({vehiculo.patente})",
                    "cantidad": cantidad_dias,
                    "monto": precio_diario
                })

        # ============================================================
        # 2) OCTUBRE — FINALIZADO — con multa y daño
        # ============================================================
        oct_extra1 = datetime(2025, 10, 15, 10, 0, 0)

        alq_oct_extra1 = AlquilerModel.create_raw(
            id_cliente=1,
            id_vehiculo=1,
            id_empleado=1,
            fecha_inicio=oct_extra1.isoformat(timespec='seconds'),
            fecha_fin_prevista=(oct_extra1 + timedelta(days=3)).isoformat(timespec='seconds'),
            fecha_fin_real=(oct_extra1 + timedelta(days=3, hours=2)).isoformat(timespec='seconds'),
            estado="finalizado"
        )

        if alq_oct_extra1:
            # Crear multa
            MultaModel.create(
                id_alquiler=alq_oct_extra1.id_alquiler,
                descripcion="Exceso de velocidad detectado",
                monto=15000,
                fecha_hora_multa=(oct_extra1 + timedelta(days=1, hours=2)).isoformat(timespec='seconds')
            )

            # Crear daño
            DanioModel.create(
                id_alquiler=alq_oct_extra1.id_alquiler,
                descripcion="Golpe en paragolpes delantero",
                costo_reparacion=45000,
                fecha_hora_reporte=(oct_extra1 + timedelta(days=3, hours=3)).isoformat(timespec='seconds')
            )

            # Calcular costo total (incluye alquiler + multa + daño)
            costo = alq_oct_extra1.calcular_y_guardar_costo()
            cantidad_dias = alq_oct_extra1.calcular_dias_alquiler()
            
            vehiculo = VehiculoService.get_by_id(alq_oct_extra1.id_vehiculo)
            precio_diario = vehiculo.precio_diario
            
            # Crear factura
            fac = FacturaService.create({
                "id_alquiler": alq_oct_extra1.id_alquiler,
                "fecha_hora_emision": oct_extra1.isoformat(timespec='seconds'),
                "monto_total": costo,
                "estado_pago": "abonado"
            })
            
            if fac:
                # Detalle 1: Alquiler (precio unitario × cantidad de días)
                DetalleFacturaService.create({
                    "id_factura": fac.id_factura,
                    "descripcion": f"Alquiler vehículo {vehiculo.marca} {vehiculo.nombre} {vehiculo.modelo} ({vehiculo.patente})",
                    "cantidad": cantidad_dias,
                    "monto": precio_diario
                })
                
                # Detalle 2: Multa
                multas = MultaService.get_by_id_alquiler(alq_oct_extra1.id_alquiler)
                if multas:
                    for multa in multas:
                        DetalleFacturaService.create({
                            "id_factura": fac.id_factura,
                            "descripcion": f"Multa: {multa.descripcion}",
                            "cantidad": 1,
                            "monto": multa.monto
                        })
                
                # Detalle 3: Daño
                danios = DanioService.get_by_id_alquiler(alq_oct_extra1.id_alquiler)
                if danios:
                    for danio in danios:
                        DetalleFacturaService.create({
                            "id_factura": fac.id_factura,
                            "descripcion": f"Daño: {danio.descripcion}",
                            "cantidad": 1,
                            "monto": danio.costo_reparacion
                        })

        # ============================================================
        # 3) OCTUBRE — FINALIZADO — sólo con daño
        # ============================================================
        oct_extra2 = datetime(2025, 10, 22, 8, 0, 0)

        alq_oct_extra2 = AlquilerModel.create_raw(
            id_cliente=2,
            id_vehiculo=3,
            id_empleado=1,
            fecha_inicio=oct_extra2.isoformat(timespec='seconds'),
            fecha_fin_prevista=(oct_extra2 + timedelta(days=1)).isoformat(timespec='seconds'),
            fecha_fin_real=(oct_extra2 + timedelta(days=1, hours=1)).isoformat(timespec='seconds'),
            estado="finalizado"
        )

        if alq_oct_extra2:
            # Crear daño
            DanioModel.create(
                id_alquiler=alq_oct_extra2.id_alquiler,
                descripcion="Rasguño lateral puerta izquierda",
                costo_reparacion=20000,
                fecha_hora_reporte=(oct_extra2 + timedelta(days=1, hours=2)).isoformat(timespec='seconds')
            )

            # Calcular costo total (incluye alquiler + daño, sin multa)
            costo = alq_oct_extra2.calcular_y_guardar_costo()
            cantidad_dias = alq_oct_extra2.calcular_dias_alquiler()
            
            vehiculo = VehiculoService.get_by_id(alq_oct_extra2.id_vehiculo)
            precio_diario = vehiculo.precio_diario
            
            # Crear factura
            fac = FacturaService.create({
                "id_alquiler": alq_oct_extra2.id_alquiler,
                "fecha_hora_emision": oct_extra2.isoformat(timespec='seconds'),
                "monto_total": costo,
                "estado_pago": "abonado"
            })
            
            if fac:
                # Detalle 1: Alquiler (precio unitario × cantidad de días)
                DetalleFacturaService.create({
                    "id_factura": fac.id_factura,
                    "descripcion": f"Alquiler vehículo {vehiculo.marca} {vehiculo.nombre} {vehiculo.modelo} ({vehiculo.patente})",
                    "cantidad": cantidad_dias,
                    "monto": precio_diario
                })
                
                # Detalle 2: Daño
                danios = DanioService.get_by_id_alquiler(alq_oct_extra2.id_alquiler)
                if danios:
                    for danio in danios:
                        DetalleFacturaService.create({
                            "id_factura": fac.id_factura,
                            "descripcion": f"Daño: {danio.descripcion}",
                            "cantidad": 1,
                            "monto": danio.costo_reparacion
                        })

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

    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="127.0.0.1", port=port, reload=True)
