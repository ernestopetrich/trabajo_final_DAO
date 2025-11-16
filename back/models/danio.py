import sqlite3
import database

class Danio:
    def __init__(self, id_danio, id_alquiler, descripcion, costo_reparacion):
        self.id_danio = id_danio
        self.id_alquiler = id_alquiler
        self.descripcion = descripcion
        self.costo_reparacion = costo_reparacion

    @staticmethod
    def create(id_alquiler, descripcion, costo_reparacion):
        conn = database.get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Danios (id_alquiler, descripcion, costo_reparacion)
            VALUES (?, ?, ?)
        """, (id_alquiler, descripcion, costo_reparacion))
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def get_all():
        conn = database.get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Danios")
        rows = cur.fetchall()
        conn.close()
        return [Danio(*row) for row in rows]

    @staticmethod
    def get_by_id(id_danio):
        conn = database.get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Danios WHERE id_danio=?", (id_danio,))
        row = cur.fetchone()
        conn.close()
        return Danio(*row) if row else None
