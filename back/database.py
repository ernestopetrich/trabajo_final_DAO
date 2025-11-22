import sqlite3
import os

DATABASE_FILE = "alquilaya.db"

class Database:
    """
    Implementación del patrón Singleton para el manejo de la base de datos.
    Asegura que la configuración y el punto de acceso sean únicos.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            # Si no existe instancia, creamos una nueva
            cls._instance = super(Database, cls).__new__(cls)
            print("--- Instancia de Database (Singleton) creada ---")
        return cls._instance

    def get_connection(self):
        """Crea y retorna una conexión a la base de datos SQLite."""
        conn = sqlite3.connect(DATABASE_FILE)
        conn.row_factory = sqlite3.Row  # Para acceder a los resultados por nombre de columna
        conn.execute("PRAGMA foreign_keys = ON;") # Habilitar llaves foráneas
        conn.execute("PRAGMA journal_mode=WAL;")
        return conn

    def create_tables(self):
        """
        Crea las tablas en la base de datos si no existen.
        """
        if os.path.exists(DATABASE_FILE):
            print("La base de datos ya existe. Verificando conexión...")
            # Podríamos hacer validaciones extra aquí si fuera necesario
        
        print("Iniciando proceso de creación/verificación de tablas...")
        conn = self.get_connection()
        cursor = conn.cursor()

        # Clientes
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Clientes (
            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo_dni TEXT NOT NULL,
            dni TEXT NOT NULL UNIQUE,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            telefono TEXT,
            email TEXT UNIQUE,
            direccion TEXT,
            estado TEXT NOT NULL DEFAULT 'activo'
        );
        """)

        # Empleados
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Empleados (
            id_empleado INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo_dni TEXT NOT NULL,
            dni TEXT NOT NULL UNIQUE,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            activo BOOLEAN NOT NULL DEFAULT 1
        );
        """)

        # Vehiculos
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Vehiculos (
            id_vehiculo INTEGER PRIMARY KEY AUTOINCREMENT,
            patente TEXT NOT NULL UNIQUE,
            marca TEXT NOT NULL,
            modelo TEXT NOT NULL,
            nombre TEXT,
            precio_diario REAL NOT NULL,
            estado TEXT NOT NULL DEFAULT 'disponible'
        );
        """)

        # Alquileres
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Alquileres (
            id_alquiler INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cliente INTEGER NOT NULL,
            id_vehiculo INTEGER NOT NULL,
            id_empleado INTEGER NOT NULL,
            fecha_hora_inicio TEXT NOT NULL,
            fecha_hora_fin_prevista TEXT NOT NULL,
            fecha_hora_fin_real TEXT,
            costo_total REAL,
            estado TEXT NOT NULL DEFAULT 'activo',
            FOREIGN KEY (id_cliente) REFERENCES Clientes (id_cliente),
            FOREIGN KEY (id_vehiculo) REFERENCES Vehiculos (id_vehiculo),
            FOREIGN KEY (id_empleado) REFERENCES Empleados (id_empleado)
        );
        """)

        # Mantenimientos
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Mantenimientos (
            id_mantenimiento INTEGER PRIMARY KEY AUTOINCREMENT,
            id_vehiculo INTEGER NOT NULL,
            fecha_hora_inicio TEXT NOT NULL,
            fecha_hora_fin TEXT,
            descripcion TEXT NOT NULL,
            costo REAL,
            FOREIGN KEY (id_vehiculo) REFERENCES Vehiculos (id_vehiculo)
        );
        """)

        # Multas
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Multas (
            id_multa INTEGER PRIMARY KEY AUTOINCREMENT,
            id_alquiler INTEGER NOT NULL,
            descripcion TEXT NOT NULL,
            monto REAL NOT NULL,
            fecha_hora_multa TEXT NOT NULL,
            estado TEXT NOT NULL DEFAULT 'pendiente',
            FOREIGN KEY (id_alquiler) REFERENCES Alquileres (id_alquiler)
        );
        """)

        # Daños
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Danios (
            id_danio INTEGER PRIMARY KEY AUTOINCREMENT,
            id_alquiler INTEGER NOT NULL,
            descripcion TEXT NOT NULL,
            costo_reparacion REAL NOT NULL,
            fecha_hora_reporte TEXT NOT NULL,
            estado TEXT NOT NULL DEFAULT 'pendiente',
            FOREIGN KEY (id_alquiler) REFERENCES Alquileres (id_alquiler)
        );
        """)

        # Facturas
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Facturas (
            id_factura INTEGER PRIMARY KEY AUTOINCREMENT,
            id_alquiler INTEGER NOT NULL,
            fecha_hora_emision TEXT NOT NULL,
            monto_total REAL NOT NULL,
            estado_pago TEXT NOT NULL DEFAULT 'pendiente',
            FOREIGN KEY (id_alquiler) REFERENCES Alquileres (id_alquiler)
        );
        """)

        # Detalle Factura
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Detalle_factura (
            id_detalle INTEGER PRIMARY KEY AUTOINCREMENT,
            id_factura INTEGER NOT NULL,
            descripcion TEXT NOT NULL, 
            monto REAL NOT NULL,
            FOREIGN KEY (id_factura) REFERENCES Facturas (id_factura)
        );
        """)

        conn.commit()
        conn.close()
        print("Tablas verificadas/creadas correctamente.")
    
    # --- MANTENEMOS ESTAS FUNCIONES COMO PUENTE ---
# Esto permite que tus modelos (alquiler.py, cliente.py, etc.) sigan funcionando
# tal cual están, pero internamente ahora usan el Singleton.

def get_db_connection():
    # Llamamos a la instancia única de Database
    return Database().get_connection()

def create_tables():
    # Llamamos al método de la instancia única
    Database().create_tables()

if __name__ == "__main__":
    Database().create_tables()