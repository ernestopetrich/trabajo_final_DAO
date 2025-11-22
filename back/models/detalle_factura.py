import sqlite3
from database import Database

class DetalleFactura:
    def __init__(self, id_detalle, id_factura, descripcion, monto):
        self.id_detalle = id_detalle
        self.id_factura = id_factura
        self.descripcion = descripcion
        self.monto = monto

    def __repr__(self):
        return f"<DetalleFactura #{self.id_detalle} (Factura: {self.id_factura}) - {self.descripcion}>"
    
    @staticmethod
    def create(id_factura, descripcion, monto):
        """Crea un nuevo detalle de factura."""
        conn = Database().get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO Detalle_Factura (id_factura, descripcion, monto) VALUES (?, ?, ?)",
                (id_factura, descripcion, monto)
            )
            conn.commit()
            return DetalleFactura.get_by_id(cursor.lastrowid)
        except sqlite3.Error as e:
            print(f"Error al crear detalle de factura: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()
    
    @staticmethod
    def get_by_id(id_detalle):
        """Obtiene un detalle de factura por su ID."""
        conn = Database().get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Detalle_Factura WHERE id_detalle = ?", (id_detalle,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return DetalleFactura(*row)
        return None
    
    @staticmethod
    def get_by_id_factura(id_factura):
        """Obtiene todos los detalles de una factura por su ID de factura."""
        conn = Database().get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Detalle_Factura WHERE id_factura = ?", (id_factura,))
        rows = cursor.fetchall()
        conn.close()
        return [DetalleFactura(*row) for row in rows]