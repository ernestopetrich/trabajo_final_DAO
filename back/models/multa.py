import sqlite3
from database import Database

class Multa:
    def __init__(self, id_multa, id_alquiler, descripcion, monto, fecha_hora_multa, estado):
        self.id_multa = id_multa
        self.id_alquiler = id_alquiler
        self.descripcion = descripcion
        self.monto = monto
        self.fecha_hora_multa = fecha_hora_multa
        self.estado = estado
    
    def __repr__(self):
        return f"<Multa #{self.id_multa} (Alquiler: {self.id_alquiler}) - {self.estado}>"
    
    @staticmethod
    def create(id_alquiler, descripcion, monto, fecha_hora_multa, estado='pendiente'):
        """Crea una nueva multa."""
        conn = Database().get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO Multas (id_alquiler, descripcion, monto, fecha_hora_multa, estado) VALUES (?, ?, ?, ?, ?)",
                (id_alquiler, descripcion, monto, fecha_hora_multa, estado)
            )
            conn.commit()
            return Multa.get_by_id(cursor.lastrowid)
        except sqlite3.Error as e:
            print(f"Error al crear multa: {e}")
            return None
        finally:
            conn.close()
    
    @staticmethod
    def get_by_id_alquiler(id_alquiler):
        """Obtiene una multa por su ID de alquiler."""
        conn = Database().get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Multas WHERE id_alquiler = ?", (id_alquiler,))
        rows = cursor.fetchall()
        conn.close()
        if rows:
            return [Multa(*row) for row in rows]
        return None
    
    @staticmethod
    def get_all():
        """Obtiene todas las multas."""
        conn = Database().get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Multas")
        rows = cursor.fetchall()
        conn.close()
        return [Multa(*row) for row in rows]
    
    @staticmethod
    def get_by_id(id_multa):
        """Obtiene una multa por su ID."""
        conn = Database().get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Multas WHERE id_multa = ?", (id_multa,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Multa(*row)
        return None