import sqlite3
import database

class DetalleFactura:
    def __init__(self, id_detalle, id_factura, descripcion, cantidad, precio_unitario):
        self.id_detalle = id_detalle
        self.id_factura = id_factura
        self.descripcion = descripcion
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario

    def __repr__(self):
        return f"<DetalleFactura #{self.id_detalle} (Factura: {self.id_factura}) - {self.descripcion}>"
    
    @staticmethod
    def create(id_factura, descripcion, cantidad, precio_unitario):
        """Crea un nuevo detalle de factura."""
        conn = database.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO Detalle_Factura (id_factura, descripcion, cantidad, precio_unitario) VALUES (?, ?, ?, ?)",
                (id_factura, descripcion, cantidad, precio_unitario)
            )
            conn.commit()
            return DetalleFactura.get_by_id(cursor.lastrowid)
        except sqlite3.Error as e:
            print(f"Error al crear detalle de factura: {e}")
            return None
        finally:
            conn.close()
    
    @staticmethod
    def get_by_id(id_detalle):
        """Obtiene un detalle de factura por su ID."""
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Detalle_Factura WHERE id_detalle = ?", (id_detalle,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return DetalleFactura(*row)
        return None