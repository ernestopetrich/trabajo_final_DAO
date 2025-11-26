import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app

client = TestClient(app)

# ==================== CLIENTES ====================

@patch('services.cliente_service.ClienteService.create')
def test_create_cliente(mock_create):
    mock_obj = MagicMock()
    mock_obj.id_cliente = 1
    mock_obj.tipo_dni = "DNI"
    mock_obj.dni = "12345678"
    mock_obj.nombre = "Juan"
    mock_obj.apellido = "Pérez"
    mock_obj.telefono = "123456789"
    mock_obj.email = "juan@example.com"
    mock_obj.direccion = "Calle Falsa 123"
    mock_obj.estado = "activo"
    mock_create.return_value = mock_obj

    response = client.post("/clientes/", json={
        "tipo_dni": "DNI",
        "dni": "12345678",
        "nombre": "Juan",
        "apellido": "Pérez",
        "telefono": "123456789",
        "email": "juan@example.com",
        "direccion": "Calle Falsa 123"
    })

    assert response.status_code == 200


@patch('services.cliente_service.ClienteService.get_all')
def test_get_clientes(mock_get_all):
    mock_get_all.return_value = []
    response = client.get("/clientes/")
    assert response.status_code == 200


@patch('services.cliente_service.ClienteService.get_by_id')
def test_get_cliente_by_id_not_found(mock_get_by_id):
    mock_get_by_id.return_value = None
    response = client.get("/clientes/999")
    assert response.status_code == 404


@patch('services.cliente_service.ClienteService.delete')
def test_delete_cliente(mock_delete):
    mock_delete.return_value = True
    response = client.put("/clientes/1/delete")
    assert response.status_code == 200


# ==================== VEHICULOS ====================

@patch('services.vehiculo_service.VehiculoService.create')
def test_create_vehiculo(mock_create):
    mock_obj = MagicMock()
    mock_obj.id_vehiculo = 1
    mock_obj.patente = "ABC123"
    mock_obj.marca = "Toyota"
    mock_obj.modelo = "Corolla"
    mock_obj.nombre = "Auto"
    mock_obj.precio_diario = 5000.0
    mock_obj.estado = "disponible"
    mock_create.return_value = mock_obj

    response = client.post("/vehiculos/", json={
        "patente": "ABC123",
        "marca": "Toyota",
        "modelo": "Corolla",
        "nombre": "Auto",
        "precio_diario": 5000.0
    })
    assert response.status_code == 200


@patch('services.vehiculo_service.VehiculoService.get_all')
def test_get_vehiculos(mock_get_all):
    mock_get_all.return_value = []
    response = client.get("/vehiculos/")
    assert response.status_code == 200


@patch('services.vehiculo_service.VehiculoService.get_by_id')
def test_get_vehiculo_not_found(mock_get_by_id):
    mock_get_by_id.return_value = None
    response = client.get("/vehiculos/999")
    assert response.status_code == 404


@patch('services.vehiculo_service.VehiculoService.delete')
def test_delete_vehiculo(mock_delete):
    mock_delete.return_value = True
    response = client.delete("/vehiculos/1")
    assert response.status_code == 200


# ==================== ALQUILERES ====================

@patch('services.alquiler_service.AlquilerService.create')
def test_create_alquiler(mock_create):
    mock_obj = MagicMock()
    mock_obj.id_alquiler = 1
    mock_obj.id_cliente = 1
    mock_obj.id_vehiculo = 1
    mock_obj.id_empleado = 1
    mock_obj.fecha_hora_inicio = "2024-01-01T00:00:00"
    mock_obj.fecha_hora_fin_prevista = "2024-01-05T00:00:00"
    mock_obj.estado = "activo"
    mock_create.return_value = mock_obj

    response = client.post("/alquileres/", json={
        "id_cliente": 1,
        "id_vehiculo": 1,
        "id_empleado": 1,
        "fecha_hora_inicio": "2024-01-01T00:00:00",
        "fecha_hora_fin_prevista": "2024-01-05T00:00:00"
    })

    assert response.status_code == 200


@patch('services.alquiler_service.AlquilerService.create')
def test_create_alquiler_error(mock_create):
    mock_create.return_value = None
    response = client.post("/alquileres/", json={
        "id_cliente": 1,
        "id_vehiculo": 1,
        "id_empleado": 1,
        "fecha_hora_inicio": "2024-01-01T00:00:00",
        "fecha_hora_fin_prevista": "2024-01-05T00:00:00"
    })
    assert response.status_code == 400


@patch('services.alquiler_service.AlquilerService.get_all')
def test_get_alquileres(mock_get_all):
    mock_get_all.return_value = []
    response = client.get("/alquileres/")
    assert response.status_code == 200


@patch('services.alquiler_service.AlquilerService.get_by_id')
def test_get_alquiler_not_found(mock_get_by_id):
    mock_get_by_id.return_value = None
    response = client.get("/alquileres/999")
    assert response.status_code == 404


@patch('services.alquiler_service.AlquilerService.devolver')
def test_devolver_alquiler(mock_devolver):
    mock_obj = MagicMock()
    mock_obj.fecha_hora_inicio = "2024-01-01T00:00:00"
    mock_obj.fecha_hora_fin_prevista = "2024-01-05T00:00:00"
    mock_obj.fecha_hora_fin_real = "2024-01-05T12:00:00"
    mock_obj.estado = "devuelto"
    mock_devolver.return_value = mock_obj

    response = client.post("/alquileres/1/devolver")
    assert response.status_code == 200


@patch('services.alquiler_service.AlquilerService.devolver')
def test_devolver_alquiler_error(mock_devolver):
    mock_devolver.return_value = None
    response = client.post("/alquileres/1/devolver")
    assert response.status_code == 400


@patch('services.alquiler_service.AlquilerService.delete')
def test_delete_alquiler(mock_delete):
    mock_delete.return_value = True
    response = client.post("/alquileres/1/delete")
    assert response.status_code == 200


# ==================== EMPLEADOS ====================

@patch('services.empleado_service.EmpleadoService.create')
def test_create_empleado(mock_create):
    mock_obj = MagicMock()
    mock_obj.id_empleado = 1
    mock_obj.tipo_dni = "DNI"
    mock_obj.dni = "11111111"
    mock_obj.nombre = "María"
    mock_obj.apellido = "González"
    mock_obj.activo = True
    mock_create.return_value = mock_obj

    response = client.post("/empleados/", json={
        "tipo_dni": "DNI",
        "dni": "11111111",
        "nombre": "María",
        "apellido": "González"
    })
    assert response.status_code == 200


@patch('services.empleado_service.EmpleadoService.get_all')
def test_get_empleados(mock_get_all):
    mock_get_all.return_value = []
    response = client.get("/empleados/")
    assert response.status_code == 200


@patch('services.empleado_service.EmpleadoService.get_by_id')
def test_get_empleado_by_id(mock_get_by_id):
    mock_obj = MagicMock()
    mock_obj.id_empleado = 1
    mock_obj.tipo_dni = "DNI"
    mock_obj.dni = "11111111"
    mock_obj.nombre = "María"
    mock_obj.apellido = "González"
    mock_obj.activo = True
    mock_get_by_id.return_value = mock_obj

    response = client.get("/empleados/1")
    assert response.status_code == 200


@patch('services.empleado_service.EmpleadoService.update')
def test_delete_empleado(mock_update):
    mock_update.return_value = {"activo": False}
    response = client.put("/empleados/1/delete")
    assert response.status_code == 200


# ==================== FACTURAS ====================

@patch('services.factura_service.FacturaService.create')
def test_create_factura(mock_create):
    mock_obj = MagicMock()
    mock_obj.id_factura = 1
    mock_obj.id_alquiler = 1
    mock_obj.fecha_hora_emision = "2024-01-01T00:00:00"
    mock_obj.monto_total = 25000.0
    mock_create.return_value = mock_obj

    response = client.post("/facturas/", json={
        "id_alquiler": 1,
        "fecha_hora_emision": "2024-01-01T00:00:00",
        "monto_total": 25000.0
    })
    assert response.status_code == 200


@patch('services.factura_service.FacturaService.get_all')
def test_get_facturas(mock_get_all):
    mock_get_all.return_value = []
    response = client.get("/facturas/")
    assert response.status_code == 200


@patch('services.factura_service.FacturaService.get_by_id')
def test_get_factura_by_id(mock_get_by_id):
    mock_obj = MagicMock()
    mock_obj.id_factura = 1
    mock_obj.id_alquiler = 1
    mock_obj.fecha_hora_emision = "2024-01-01T00:00:00"
    mock_obj.monto_total = 25000.0
    mock_get_by_id.return_value = mock_obj

    response = client.get("/facturas/1")
    assert response.status_code == 200


# ==================== DAÑOS ====================

@patch('services.danio_service.DanioService.create')
def test_create_danio(mock_create):
    mock_obj = MagicMock()
    mock_obj.id_danio = 1
    mock_obj.id_alquiler = 1
    mock_obj.descripcion = "Rayón"
    mock_obj.costo_reparacion = 5000.0
    mock_obj.fecha_hora_reporte = "2024-01-01T12:00:00"
    mock_obj.estado = "reportado"
    mock_create.return_value = mock_obj

    response = client.post("/danios/", json={
        "id_alquiler": 1,
        "descripcion": "Rayón",
        "costo_reparacion": 5000.0,
        "fecha_hora_reporte": "2024-01-01T12:00:00"
    })
    assert response.status_code == 200


@patch('services.danio_service.DanioService.get_all')
def test_get_danios(mock_get_all):
    mock_get_all.return_value = []
    response = client.get("/danios/")
    assert response.status_code == 200


@patch('services.danio_service.DanioService.get_by_id_alquiler')
def test_get_danios_por_alquiler(mock_get_by_alquiler):
    mock_get_by_alquiler.return_value = []
    response = client.get("/danios/alquiler/1")
    assert response.status_code == 200


# ==================== MULTAS ====================

@patch('services.multa_service.MultaService.create')
def test_create_multa(mock_create):
    mock_obj = MagicMock()
    mock_obj.id_multa = 1
    mock_obj.id_alquiler = 1
    mock_obj.descripcion = "Exceso"
    mock_obj.monto = 10000.0
    mock_obj.fecha_hora_multa = "2024-01-02T15:00:00"
    mock_obj.estado = "pendiente"
    mock_create.return_value = mock_obj

    response = client.post("/multas/", json={
        "id_alquiler": 1,
        "descripcion": "Exceso",
        "monto": 10000.0,
        "fecha_hora_multa": "2024-01-02T15:00:00"
    })
    assert response.status_code == 200


@patch('services.multa_service.MultaService.get_all')
def test_get_multas(mock_get_all):
    mock_get_all.return_value = []
    response = client.get("/multas/")
    assert response.status_code == 200


@patch('services.multa_service.MultaService.get_by_id_alquiler')
def test_get_multas_por_alquiler(mock_get_by_alquiler):
    mock_get_by_alquiler.return_value = []
    response = client.get("/multas/alquiler/1")
    assert response.status_code == 200


# ==================== MANTENIMIENTOS ====================

@patch('services.mantenimiento_service.MantenimientoService.create')
def test_create_mantenimiento(mock_create):
    mock_obj = MagicMock()
    mock_obj.id_mantenimiento = 1
    mock_obj.id_vehiculo = 1
    mock_obj.fecha_hora_inicio = "2024-01-15T09:00:00"
    mock_obj.fecha_hora_fin = None
    mock_obj.descripcion = "Cambio de aceite"
    mock_obj.costo = 3000.0
    mock_create.return_value = mock_obj

    response = client.post("/mantenimientos/", json={
        "id_vehiculo": 1,
        "fecha_hora_inicio": "2024-01-15T09:00:00",
        "descripcion": "Cambio de aceite",
        "costo": 3000.0
    })
    assert response.status_code == 200


@patch('services.mantenimiento_service.MantenimientoService.get_all')
def test_get_mantenimientos(mock_get_all):
    mock_get_all.return_value = []
    response = client.get("/mantenimientos/")
    assert response.status_code == 200


@patch('services.mantenimiento_service.MantenimientoService.get_by_id')
def test_get_mantenimiento_by_id(mock_get_by_id):
    mock_obj = MagicMock()
    mock_obj.id_mantenimiento = 1
    mock_obj.id_vehiculo = 1
    mock_obj.fecha_hora_inicio = "2024-01-15T09:00:00"
    mock_obj.fecha_hora_fin = "2024-01-15T11:00:00"
    mock_obj.descripcion = "Cambio de aceite"
    mock_obj.costo = 3000.0
    mock_get_by_id.return_value = mock_obj

    response = client.get("/mantenimientos/1")
    assert response.status_code == 200


@patch('services.mantenimiento_service.MantenimientoService.get_by_id')
def test_get_mantenimiento_not_found(mock_get_by_id):
    mock_get_by_id.return_value = None
    response = client.get("/mantenimientos/999")
    assert response.status_code == 404


# ==================== REPORTES ====================

@patch('services.reporte_service.ReportesService.reporte_flota')
def test_reporte_flota_pdf(mock_reporte):
    from io import BytesIO
    mock_reporte.return_value = BytesIO(b"PDF OK")
    response = client.get("/reportes/flota/pdf")
    assert response.status_code == 200


@patch('services.reporte_service.ReportesService.reporte_alquileres_por_cliente')
def test_reporte_alquileres_cliente(mock_reporte):
    from io import BytesIO
    mock_reporte.return_value = BytesIO(b"PDF OK")
    response = client.get("/reportes/pdf/alquileres-por-cliente")
    assert response.status_code == 200


@patch('services.reporte_service.ReportesService.reporte_ranking_vehiculos')
def test_reporte_ranking_vehiculos(mock_reporte):
    from io import BytesIO
    mock_reporte.return_value = BytesIO(b"PDF OK")
    response = client.get("/reportes/pdf/vehiculos-mas-alquilados")
    assert response.status_code == 200


@patch('services.reporte_service.ReportesService.reporte_alquileres_mensuales')
def test_reporte_alquileres_mensuales(mock_reporte):
    from io import BytesIO
    mock_reporte.return_value = BytesIO(b"PDF OK")
    response = client.get("/reportes/pdf/alquileres-por-mes")
    assert response.status_code == 200


@patch('services.reporte_service.ReportesService.reporte_facturacion_mensual')
def test_reporte_facturacion_mensual(mock_reporte):
    from io import BytesIO
    mock_reporte.return_value = BytesIO(b"PDF OK")
    response = client.get("/reportes/pdf/facturacion-mensual")
    assert response.status_code == 200
