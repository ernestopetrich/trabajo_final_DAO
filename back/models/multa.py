import sqlite3
import database

class Multa:
    def __init__(self, id_multa, id_alquiler, monto, descripcion):
        self.id_multa = id_multa
        self.id_alquiler = id_alquiler
        self.monto = monto
        self.descripcion = descripcion

    @staticmethod
    def create(id_alquiler, monto, descripcion):
        conn = database.get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Multas (id_alquiler, monto, descripcion)
            VALUES (?, ?, ?)
        """, (id_alquiler, monto, descripcion))
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def get_all():
        conn = database.get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Multas")
        rows = cur.fetchall()
        conn.close()
        return [Multa(*row) for row in rows]

    @staticmethod
    def get_by_id(id_multa):
        conn = database.get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Multas WHERE id_multa=?", (id_multa,))
        row = cur.fetchone()
        conn.close()
        return Multa(*row) if row else None
