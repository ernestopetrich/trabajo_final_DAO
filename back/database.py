import sqlite3
import os

DATABASE_FILE = "alquilaya.db"

def get_db_connection():
    """Crea y retorna una conexión a la base de datos SQLite."""
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row  # Para acceder a los resultados por nombre de columna
    conn.execute("PRAGMA foreign_keys = ON;") # Habilitar llaves foráneas
    return conn

def create_tables():
    """
    Crea las tablas en la base de datos si no existen.
    Basado en el DER y añadiendo la tabla de Reservas.
    """
    if os.path.exists(DATABASE_FILE):
        print("La base de datos ya existe. No se crearán tablas de nuevo.")
        return

    print("Creando base de datos y tablas...")
    conn = get_db_connection()
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
        direccion TEXT
    );
    """)

    # Empleados
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Empleados (
        id_empleado INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo_dni TEXT NOT NULL,
        dni TEXT NOT NULL UNIQUE,
        nombre TEXT NOT NULL,
        apellido TEXT NOT NULL
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
        -- Estados: disponible, alquilado, mantenimiento
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
        -- Estados: activo, finalizado, cancelado
        FOREIGN KEY (id_cliente) REFERENCES Clientes (id_cliente),
        FOREIGN KEY (id_vehiculo) REFERENCES Vehiculos (id_vehiculo),
        FOREIGN KEY (id_empleado) REFERENCES Empleados (id_empleado)
    );
    """)

    # Reservas (¡NUEVA TABLA SOLICITADA!)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Reservas (
        id_reserva INTEGER PRIMARY KEY AUTOINCREMENT,
        id_cliente INTEGER NOT NULL,
        id_vehiculo INTEGER NOT NULL,
        fecha_inicio TEXT NOT NULL,
        fecha_fin TEXT NOT NULL,
        estado TEXT NOT NULL DEFAULT 'pendiente',
        -- Estados: pendiente, confirmada, cancelada, completada
        FOREIGN KEY (id_cliente) REFERENCES Clientes (id_cliente),
        FOREIGN KEY (id_vehiculo) REFERENCES Vehiculos (id_vehiculo)
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

    # Danios
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
    
    # Facturas (Faltaría Detalle_Factura, pero lo omitimos por simplicidad inicial)
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

    conn.commit()
    conn.close()
    print("Tablas creadas exitosamente.")

if __name__ == "__main__":
    create_tables()