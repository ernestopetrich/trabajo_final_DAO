import sqlite3
import database

class DetalleFactura:
    def __init__(self, id_detalle, id_factura, descripcion, monto):
        self.id_detalle = id_detalle
        self.id_factura = id_factura
        self.descripcion = descripcion
        self.monto = monto

    @staticmethod
    def create(id_factura, descripcion, monto):
        conn = database.get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO DetalleFacturas (id_factura, descripcion, monto)
            VALUES (?, ?, ?)
        """, (id_factura, descripcion, monto))
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def get_all_for_factura(id_factura):
        conn = database.get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM DetalleFacturas WHERE id_factura=?", (id_factura,))
        rows = cur.fetchall()
        conn.close()
        return [DetalleFactura(*row) for row in rows]
