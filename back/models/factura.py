import sqlite3
import database

class Factura:
    def __init__(self, id_factura, id_alquiler, fecha_hora_emision, monto_total, estado_pago):
        self.id_factura = id_factura
        self.id_alquiler = id_alquiler
        self.fecha_hora_emision = fecha_hora_emision
        self.monto_total = monto_total
        self.estado_pago = estado_pago

    def __repr__(self):
        return f"<Factura #{self.id_factura} (Alquiler: {self.id_alquiler}) - {self.estado_pago}>"
    
    @staticmethod
    def create(id_alquiler, fecha_hora_emision, monto_total, estado_pago='pendiente'):
        """Crea una nueva factura."""
        conn = database.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO Facturas (id_alquiler, fecha_hora_emision, monto_total, estado_pago) VALUES (?, ?, ?, ?)",
                (id_alquiler, fecha_hora_emision, monto_total, estado_pago)
            )
            conn.commit()
            return Factura.get_by_id(cursor.lastrowid)
        except sqlite3.Error as e:
            print(f"Error al crear factura: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_id(id_factura):
        """Obtiene una factura por su ID."""
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Facturas WHERE id_factura = ?", (id_factura,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Factura(*row)
        return None

    @staticmethod
    def get_all():
        """Obtiene todas las facturas."""
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Facturas")
        rows = cursor.fetchall()
        conn.close()
        return [Factura(*row) for row in rows]