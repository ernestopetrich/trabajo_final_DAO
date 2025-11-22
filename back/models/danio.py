import sqlite3
from database import Database

class Danio:
    def __init__(self, id_danio, id_alquiler, descripcion, costo_reparacion, fecha_hora_reporte, estado):
        self.id_danio = id_danio
        self.id_alquiler = id_alquiler
        self.descripcion = descripcion
        self.costo_reparacion = costo_reparacion
        self.fecha_hora_reporte = fecha_hora_reporte
        self.estado = estado

    def __repr__(self):
        return f"<Danio #{self.id_danio} (Alquiler: {self.id_alquiler}) - {self.estado}>"
    
    @staticmethod
    def create(id_alquiler, descripcion, costo_reparacion, fecha_hora_reporte, estado='pendiente'):
        """Crea un nuevo daño."""
        conn = Database().get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO Danios (id_alquiler, descripcion, costo_reparacion, fecha_hora_reporte, estado) VALUES (?, ?, ?, ?, ?)",
                (id_alquiler, descripcion, costo_reparacion, fecha_hora_reporte, estado)
            )
            conn.commit()
            return Danio.get_by_id(cursor.lastrowid)
        except sqlite3.Error as e:
            print(f"Error al crear daño: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()
        
    @staticmethod
    def get_by_id_alquiler(id_alquiler):
        """Obtiene un daño por su ID de alquiler."""
        conn = Database().get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Danios WHERE id_alquiler = ?", (id_alquiler,))
        rows = cursor.fetchall()
        conn.close()
        if rows:
            return [Danio(*row) for row in rows]
        return None
    
    @staticmethod
    def get_all():
        """Obtiene todos los daños."""
        conn = Database().get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Danios")
        rows = cursor.fetchall()
        conn.close()
        return [Danio(*row) for row in rows]
 