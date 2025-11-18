import sqlite3
import database

class Empleado:
    def __init__(self, id_empleado, tipo_dni, dni, nombre, apellido):
        self.id_empleado = id_empleado
        self.tipo_dni = tipo_dni
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido

    def __repr__(self):
        return f"<Empleado {self.nombre} {self.apellido} (DNI: {self.dni})>"

    @staticmethod
    def create(tipo_dni, dni, nombre, apellido):
        """Crea un nuevo empleado en la BD."""
        conn = database.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO Empleados (tipo_dni, dni, nombre, apellido) VALUES (?, ?, ?, ?)",
                (tipo_dni, dni, nombre, apellido)
            )
            conn.commit()
            return Empleado.get_by_id(cursor.lastrowid)
        except sqlite3.IntegrityError as e:
            print(f"Error al crear empleado: {e}")
            return None
        finally:
            conn.close()
        
    @staticmethod
    def get_all():
        """Obtiene todos los empleados."""
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Empleados")
        rows = cursor.fetchall()
        conn.close()
        return [Empleado(*row) for row in rows]

    @staticmethod
    def get_by_id(id_empleado):
        """Obtiene un empleado por su ID."""
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Empleados WHERE id_empleado = ?", (id_empleado,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Empleado(*row)
        return None
    
    @staticmethod
    def get_by_dni(dni):
        """Obtiene un empleado por su DNI."""
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Empleados WHERE dni = ?", (dni,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Empleado(*row)
        return None

