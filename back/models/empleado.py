import sqlite3
import database

class Empleado:
    def __init__(self, id_empleado, tipo_dni, dni, nombre, apellido):
        self.id_empleado = id_empleado
        self.tipo_dni = tipo_dni
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido

    @staticmethod
    def create(tipo_dni, dni, nombre, apellido):
        conn = database.get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO Empleados (tipo_dni, dni, nombre, apellido)
                VALUES (?, ?, ?, ?)
            """, (tipo_dni, dni, nombre, apellido))
            conn.commit()
            return Empleado.get_by_id(cur.lastrowid)
        except sqlite3.IntegrityError:
            return None
        finally:
            conn.close()

    @staticmethod
    def get_all():
        conn = database.get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Empleados")
        rows = cur.fetchall()
        conn.close()
        return [Empleado(*row) for row in rows]

    @staticmethod
    def get_by_id(id_empleado):
        conn = database.get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Empleados WHERE id_empleado=?", (id_empleado,))
        row = cur.fetchone()
        conn.close()
        return Empleado(*row) if row else None
