import sqlite3
import database

class Reserva:
    def __init__(self, id_reserva, id_cliente, id_vehiculo, fecha_inicio, fecha_fin, estado, precio_estimado):
        self.id_reserva = id_reserva
        self.id_cliente = id_cliente
        self.id_vehiculo = id_vehiculo
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.estado = estado
        self.precio_estimado = precio_estimado

    @staticmethod
    def create(id_cliente, id_vehiculo, fecha_inicio, fecha_fin, estado, precio_estimado):
        conn = database.get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Reservas (id_cliente, id_vehiculo, fecha_inicio, fecha_fin, estado, precio_estimado)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (id_cliente, id_vehiculo, fecha_inicio, fecha_fin, estado, precio_estimado))
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def get_all():
        conn = database.get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Reservas")
        rows = cur.fetchall()
        conn.close()
        return [Reserva(*row) for row in rows]

    @staticmethod
    def get_by_id(id_reserva):
        conn = database.get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Reservas WHERE id_reserva=?", (id_reserva,))
        row = cur.fetchone()
        conn.close()
        return Reserva(*row) if row else None
