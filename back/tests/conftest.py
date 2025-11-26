import sys
import os

# Agregamos la carpeta raíz del proyecto ("..") al path de Python
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

import pytest
import sqlite3
from database import Database
from main import app
from fastapi.testclient import TestClient

# --- CLASE WRAPPER PARA LA CONEXIÓN ---
class ConnectionWrapper:
    """
    Envuelve la conexión real de SQLite para interceptar el método .close().
    En los tests, queremos que la conexión en memoria siga viva aunque
    los modelos (Cliente, Alquiler, etc.) llamen a .close().
    """
    def __init__(self, original_connection):
        self.original_connection = original_connection

    def close(self):
        # ¡TRUCO! No hacemos nada. Ignoramos la orden de cierre del modelo.
        # La conexión real se cerrará solo al final del test (en el fixture).
        pass

    def __getattr__(self, name):
        # Delegamos cualquier otro método (cursor, commit, execute) a la conexión real
        return getattr(self.original_connection, name)

# --- FIXTURE DE BASE DE DATOS ---
@pytest.fixture(scope="function", autouse=True)
def test_db():
    """
    Crea una base de datos SQLite en memoria para cada test.
    Sobrescribe el Singleton Database para que use esta conexión.
    """
    # 1. Crear conexión REAL en memoria
    real_connection = sqlite3.connect(":memory:")
    real_connection.row_factory = sqlite3.Row
    real_connection.execute("PRAGMA foreign_keys = ON;")
    
    # 2. Envolverla para protegerla de cierres prematuros
    safe_connection = ConnectionWrapper(real_connection)
    
    # 3. Crear las tablas
    cursor = real_connection.cursor()
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS Clientes (
            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo_dni TEXT NOT NULL, dni TEXT NOT NULL UNIQUE, nombre TEXT NOT NULL,
            apellido TEXT NOT NULL, telefono TEXT, email TEXT UNIQUE, direccion TEXT,
            estado TEXT NOT NULL DEFAULT 'activo'
        );
        CREATE TABLE IF NOT EXISTS Empleados (
            id_empleado INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo_dni TEXT NOT NULL, dni TEXT NOT NULL UNIQUE, nombre TEXT NOT NULL,
            apellido TEXT NOT NULL, activo BOOLEAN NOT NULL DEFAULT 1
        );
        CREATE TABLE IF NOT EXISTS Vehiculos (
            id_vehiculo INTEGER PRIMARY KEY AUTOINCREMENT,
            patente TEXT NOT NULL UNIQUE, marca TEXT NOT NULL, modelo TEXT NOT NULL,
            nombre TEXT, precio_diario REAL NOT NULL, estado TEXT NOT NULL DEFAULT 'disponible'
        );
        CREATE TABLE IF NOT EXISTS Alquileres (
            id_alquiler INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cliente INTEGER NOT NULL, id_vehiculo INTEGER NOT NULL, id_empleado INTEGER NOT NULL,
            fecha_hora_inicio TEXT NOT NULL, fecha_hora_fin_prevista TEXT NOT NULL,
            fecha_hora_fin_real TEXT, costo_total REAL, estado TEXT NOT NULL DEFAULT 'activo',
            FOREIGN KEY (id_cliente) REFERENCES Clientes (id_cliente),
            FOREIGN KEY (id_vehiculo) REFERENCES Vehiculos (id_vehiculo),
            FOREIGN KEY (id_empleado) REFERENCES Empleados (id_empleado)
        );
        CREATE TABLE IF NOT EXISTS Mantenimientos (
            id_mantenimiento INTEGER PRIMARY KEY AUTOINCREMENT, id_vehiculo INTEGER NOT NULL,
            fecha_hora_inicio TEXT NOT NULL, fecha_hora_fin TEXT, descripcion TEXT NOT NULL, costo REAL,
            FOREIGN KEY (id_vehiculo) REFERENCES Vehiculos (id_vehiculo)
        );
        CREATE TABLE IF NOT EXISTS Multas (
            id_multa INTEGER PRIMARY KEY AUTOINCREMENT, id_alquiler INTEGER NOT NULL,
            descripcion TEXT NOT NULL, monto REAL NOT NULL, fecha_hora_multa TEXT NOT NULL,
            estado TEXT NOT NULL DEFAULT 'pendiente',
            FOREIGN KEY (id_alquiler) REFERENCES Alquileres (id_alquiler)
        );
        CREATE TABLE IF NOT EXISTS Danios (
            id_danio INTEGER PRIMARY KEY AUTOINCREMENT, id_alquiler INTEGER NOT NULL,
            descripcion TEXT NOT NULL, costo_reparacion REAL NOT NULL, fecha_hora_reporte TEXT NOT NULL,
            estado TEXT NOT NULL DEFAULT 'pendiente',
            FOREIGN KEY (id_alquiler) REFERENCES Alquileres (id_alquiler)
        );
        CREATE TABLE IF NOT EXISTS Facturas (
            id_factura INTEGER PRIMARY KEY AUTOINCREMENT, id_alquiler INTEGER NOT NULL,
            fecha_hora_emision TEXT NOT NULL, monto_total REAL NOT NULL,
            estado_pago TEXT NOT NULL DEFAULT 'pendiente',
            FOREIGN KEY (id_alquiler) REFERENCES Alquileres (id_alquiler)
        );
        CREATE TABLE IF NOT EXISTS Detalle_factura (
            id_detalle INTEGER PRIMARY KEY AUTOINCREMENT, id_factura INTEGER NOT NULL,
            descripcion TEXT NOT NULL, cantidad INTEGER NOT NULL DEFAULT 1, monto REAL NOT NULL,
            FOREIGN KEY (id_factura) REFERENCES Facturas (id_factura)
        );
    """)
    real_connection.commit()

    # 4. MONKEY PATCHING: Reemplazar el método del Singleton
    original_method = Database.get_connection
    
    def mock_get_connection(self):
        # Devolvemos la conexión "segura" que ignora los close()
        return safe_connection
    
    Database.get_connection = mock_get_connection

    # Ejecutamos el test
    yield safe_connection

    # 5. Limpieza Real
    real_connection.close() # Ahora sí cerramos la conexión de verdad
    Database.get_connection = original_method # Restauramos el método original

# --- FIXTURE DEL CLIENTE API ---
@pytest.fixture
def client():
    """Devuelve un cliente de pruebas de FastAPI."""
    return TestClient(app)