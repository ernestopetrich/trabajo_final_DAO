import sqlite3
import database

class Factura:
    def __init__(self, id_factura, id_alquiler, fecha_emision, monto_total):
        self.id_factura = id_factura
        self.id_alquiler = id_alquiler
        self.fecha_emision = fecha_emision
        self.monto_total = monto_total

    @staticmethod
    def create(id_alquiler, fecha_emision, monto_total):
        conn = database.get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Facturas (id_alquiler, fecha_emision, monto_total)
            VALUES (?, ?, ?)
        """, (id_alquiler, fecha_emision, monto_total))
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def get_by_id(id_factura):
        conn = database.get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Facturas WHERE id_factura=?", (id_factura,))
        row = cur.fetchone()
        conn.close()
        return Factura(*row) if row else None

    @staticmethod
    def get_all():
        conn = database.get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Facturas")
        rows = cur.fetchall()
        conn.close()
        return [Factura(*row) for row in rows]
