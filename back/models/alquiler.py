import sqlite3
import database

class Alquiler:
    def __init__(self, id_alquiler, id_reserva, fecha_inicio, fecha_fin, precio_total, estado):
        self.id_alquiler = id_alquiler
        self.id_reserva = id_reserva
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.precio_total = precio_total
        self.estado = estado

    @staticmethod
    def create(id_reserva, fecha_inicio, fecha_fin, precio_total, estado):
        conn = database.get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Alquileres (id_reserva, fecha_inicio, fecha_fin, precio_total, estado)
            VALUES (?, ?, ?, ?, ?)
        """, (id_reserva, fecha_inicio, fecha_fin, precio_total, estado))
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def get_by_id(id_alquiler):
        conn = database.get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Alquileres WHERE id_alquiler=?", (id_alquiler,))
        row = cur.fetchone()
        conn.close()
        return Alquiler(*row) if row else None

    @staticmethod
    def get_all():
        conn = database.get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Alquileres")
        rows = cur.fetchall()
        conn.close()
        return [Alquiler(*row) for row in rows]
