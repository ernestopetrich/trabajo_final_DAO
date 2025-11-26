import pytest
from datetime import datetime, timedelta
from models.alquiler import Alquiler
from models.vehiculo import Vehiculo
from models.cliente import Cliente
from models.empleado import Empleado

def setup_datos_base():
    """Helper para crear datos necesarios para alquilar."""
    c = Cliente.create("DNI", "111", "Test", "Cliente", "123", "test@mail.com", "Dir")
    e = Empleado.create("DNI", "222", "Test", "Empleado")
    v = Vehiculo.create("AAA111", "Fiat", "Uno", "Base", 1000.0) # Precio $1000 por día
    return c, e, v

def test_calculo_costo_alquiler():
    """Verifica que el cálculo matemático del alquiler sea correcto."""
    cliente, empleado, vehiculo = setup_datos_base()
    
    # Simulamos un alquiler hace 3 días
    fecha_inicio = (datetime.now() - timedelta(days=3)).isoformat()
    fecha_fin_prevista = (datetime.now() + timedelta(days=1)).isoformat()
    
    alquiler = Alquiler.create(cliente.id_cliente, vehiculo.id_vehiculo, empleado.id_empleado, fecha_inicio, fecha_fin_prevista)
    
    assert alquiler.estado == "pendiente"

    # Ejecutamos la confirmación
    alquiler.confirmar()
    assert alquiler.estado == "confirmado"

    # Iniciamos el alquiler
    alquiler.iniciar()
    assert alquiler.estado == "activo"

    v = Vehiculo.get_by_id(vehiculo.id_vehiculo)
    assert v.estado == "alquilado"
    


    # Ejecutamos la devolución (esto dispara el cálculo)
    alquiler.devolver()
    
    # VERIFICACIONES
    # 1. El estado debe haber cambiado
    assert alquiler.estado == "finalizado"
    
    # 2. El costo debe ser: 3 días (aprox) * 1000 = 3000 
    # (o 4 si ceil redondeó el momento exacto de creación)
    assert alquiler.costo_total >= 3000.0
    
    # 3. El vehículo debe estar disponible de nuevo
    v_actualizado = Vehiculo.get_by_id(vehiculo.id_vehiculo)
    assert v_actualizado.estado == "disponible"

def test_state_pattern_restricciones():
    """Verifica que el patrón State impida acciones ilegales."""
    cliente, empleado, vehiculo = setup_datos_base()
    fecha_inicio = (datetime.now() - timedelta(days=3)).isoformat()
    fecha_fin = (datetime.now() + timedelta(days=3)).isoformat()
    
    alquiler = Alquiler.create(cliente.id_cliente, vehiculo.id_vehiculo, empleado.id_empleado, fecha_inicio, fecha_fin)
    
    
    alquiler.confirmar()
    alquiler.iniciar()    
    # Intentar iniciar un alquiler que ya está activo debería fallar

    try:
        alquiler.iniciar() # Un activo no se puede iniciar de nuevo
        assert False, "Debería haber lanzado error"
    except ValueError as e:
        assert "No se puede iniciar" in str(e)

    # Finalizamos
    alquiler.devolver()
    
    # Intentar devolver algo ya finalizado
    try:
        alquiler.devolver()
        assert False, "Debería haber lanzado error"
    except ValueError as e:
        assert "No se puede devolver" in str(e)