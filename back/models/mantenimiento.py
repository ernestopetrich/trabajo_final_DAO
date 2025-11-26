import sqlite3
from database import Database

class Mantenimiento:
    def __init__(self, id_mantenimiento, id_vehiculo, fecha_hora_inicio, fecha_hora_fin, descripcion, costo):
        self.id_mantenimiento = id_mantenimiento
        self.id_vehiculo = id_vehiculo
        self.fecha_hora_inicio = fecha_hora_inicio
        self.fecha_hora_fin = fecha_hora_fin
        self.descripcion = descripcion
        self.costo = costo

    def __repr__(self):
        return f"<Mantenimiento #{self.id_mantenimiento} (Veh: {self.id_vehiculo}) - {self.estado}>"
    
    @staticmethod
    def create(id_vehiculo, fecha_hora_inicio, descripcion, costo):
        """Crea un nuevo registro de mantenimiento."""
        conn = Database().get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO Mantenimientos (id_vehiculo, fecha_hora_inicio, descripcion, costo) VALUES (?, ?, ?, ?)",
                (id_vehiculo, fecha_hora_inicio, descripcion, costo)
            )
            conn.commit()
            return Mantenimiento.get_by_id(cursor.lastrowid)
        except sqlite3.Error as e:
            print(f"Error al crear mantenimiento: {e}")
            return None
        finally:
            conn.close()
        
    @staticmethod
    def get_by_id(id_mantenimiento):
        """Obtiene un mantenimiento por su ID."""
        conn = Database().get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Mantenimientos WHERE id_mantenimiento = ?", (id_mantenimiento,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Mantenimiento(*row)
        return None
    
    @staticmethod
    def get_all():
        """Obtiene todos los mantenimientos."""
        conn = Database().get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Mantenimientos")
        rows = cursor.fetchall()
        conn.close()
        return [Mantenimiento(*row) for row in rows]
    
    @staticmethod
    def update(id_mantenimiento, **fields):
        """Actualiza un registro de mantenimiento."""
        conn = Database().get_connection()
        cursor = conn.cursor()
        query_fields = []
        params = []

        for key, value in fields.items():
            query_fields.append(f"{key} = ?")
            params.append(value)

        if not query_fields:
            return Mantenimiento.get_by_id(id_mantenimiento)

        params.append(id_mantenimiento)

        try:
            cursor.execute(
                f"UPDATE Mantenimientos SET {', '.join(query_fields)} WHERE id_mantenimiento = ?",
                params
            )
            conn.commit()
            return Mantenimiento.get_by_id(id_mantenimiento)
        except sqlite3.Error as e:
            print(f"Error al actualizar mantenimiento: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_active_by_vehiculo(id_vehiculo):
        """Obtiene los mantenimientos activos (sin fecha de fin) para un vehículo."""
        conn = Database().get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM Mantenimientos WHERE id_vehiculo = ? AND fecha_hora_fin IS NULL",
            (id_vehiculo,)
        )
        row = cursor.fetchone()
        conn.close()
        if row:
            return Mantenimiento(*row)
        return None