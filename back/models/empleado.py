import sqlite3
from database import Database

class Empleado:
    def __init__(self, id_empleado, tipo_dni, dni, nombre, apellido, activo=1):
        self.id_empleado = id_empleado
        self.tipo_dni = tipo_dni
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.activo = activo

    def __repr__(self):
        return f"<Empleado {self.nombre} {self.apellido} (DNI: {self.dni})>"

    @staticmethod
    def create(tipo_dni, dni, nombre, apellido):
        """Crea un nuevo empleado en la BD."""
        conn = Database().get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO Empleados (tipo_dni, dni, nombre, apellido, activo) VALUES (?, ?, ?, ?, 1)",
                (tipo_dni, dni, nombre, apellido)
            )
            conn.commit()
            return Empleado.get_by_id(cursor.lastrowid)
        except sqlite3.IntegrityError as e:
            print(f"Error al crear empleado: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()
        
    @staticmethod
    def get_all():
        """Obtiene todos los empleados."""
        conn = Database().get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Empleados")
        rows = cursor.fetchall()
        conn.close()
        return [Empleado(*row) for row in rows]

    @staticmethod
    def get_by_id(id_empleado):
        """Obtiene un empleado por su ID."""
        conn = Database().get_connection()
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
        conn = Database().get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Empleados WHERE dni = ?", (dni,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Empleado(*row)
        return None
    
    @staticmethod
    def update(id_empleado, **fields):
        """Actualiza un empleado existente."""
        conn = Database().get_connection()
        cursor = conn.cursor()

        # Filtrar campos válidos (evita columnas inexistentes)
        valid_fields = {k: v for k, v in fields.items() if v is not None}

        if not valid_fields:
            conn.close()
            return Empleado.get_by_id(id_empleado)

        query_fields = [f"{k}=?" for k in valid_fields.keys()]
        query = f"UPDATE Empleados SET {', '.join(query_fields)} WHERE id_empleado = ?"
        values = list(valid_fields.values()) + [id_empleado]
        print(query_fields)
        print(values)
        try:
            cursor.execute(query, values)
            conn.commit()
            return Empleado.get_by_id(id_empleado)
        except sqlite3.Error as e:
            print(f"Error al actualizar empleado: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()

