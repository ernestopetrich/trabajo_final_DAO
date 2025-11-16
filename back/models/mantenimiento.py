import sqlite3
import database

class Mantenimiento:
    def __init__(self, id_mantenimiento, id_vehiculo, fecha, costo, descripcion):
        self.id_mantenimiento = id_mantenimiento
        self.id_vehiculo = id_vehiculo
        self.fecha = fecha
        self.costo = costo
        self.descripcion = descripcion

    @staticmethod
    def create(id_vehiculo, fecha, costo, descripcion):
        conn = database.get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Mantenimientos (id_vehiculo, fecha, costo, descripcion)
            VALUES (?, ?, ?, ?)
        """, (id_vehiculo, fecha, costo, descripcion))
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def get_all():
        conn = database.get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Mantenimientos")
        rows = cur.fetchall()
        conn.close()
        return [Mantenimiento(*row) for row in rows]

    @staticmethod
    def get_by_id(id_mantenimiento):
        conn = database.get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Mantenimientos WHERE id_mantenimiento=?", (id_mantenimiento,))
        row = cur.fetchone()
        conn.close()
        return Mantenimiento(*row) if row else None
