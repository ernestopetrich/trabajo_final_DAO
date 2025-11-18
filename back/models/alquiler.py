import sqlite3
import database

class Alquiler:
    def __init__(self, id_alquiler, id_cliente, id_vehiculo, id_empleado, fecha_hora_inicio, 
                 fecha_hora_fin_prevista, fecha_hora_fin_real, costo_total, estado):
        self.id_alquiler = id_alquiler
        self.id_cliente = id_cliente
        self.id_vehiculo = id_vehiculo
        self.id_empleado = id_empleado
        self.fecha_hora_inicio = fecha_hora_inicio
        self.fecha_hora_fin_prevista = fecha_hora_fin_prevista
        self.fecha_hora_fin_real = fecha_hora_fin_real
        self.costo_total = costo_total
        self.estado = estado

    def __repr__(self):
        return f"<Alquiler #{self.id_alquiler} (Veh: {self.id_vehiculo}) - {self.estado}>"

    @staticmethod
    def create(id_cliente, id_vehiculo, id_empleado, fecha_hora_inicio, fecha_hora_fin_prevista):
        """Crea un nuevo alquiler y marca el vehículo como 'alquilado'."""
        
        # 1. Crear el registro de alquiler
        conn = database.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO Alquileres (id_cliente, id_vehiculo, id_empleado, fecha_hora_inicio, fecha_hora_fin_prevista, estado) VALUES (?, ?, ?, ?, ?, ?)",
                (id_cliente, id_vehiculo, id_empleado, fecha_hora_inicio, fecha_hora_fin_prevista, 'activo')
            )
            id_alquiler = cursor.lastrowid
            
            # 2. Actualizar estado del vehículo
            cursor.execute("UPDATE Vehiculos SET estado = 'alquilado' WHERE id_vehiculo = ?", (id_vehiculo,))
            
            conn.commit()
            return Alquiler.get_by_id(id_alquiler)
        except sqlite3.Error as e:
            print(f"Error al crear alquiler: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_id(id_alquiler):
        """Obtiene un alquiler por su ID."""
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Alquileres WHERE id_alquiler = ?", (id_alquiler,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Alquiler(*row)
        return None
    
    @staticmethod
    def get_all():
        """Obtiene todos los alquileres."""
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Alquileres")
        rows = cursor.fetchall()
        conn.close()
        return [Alquiler(*row) for row in rows]
    
    
    def update_estado(self, nuevo_estado):
        """Actualiza el estado del alquiler (ej. 'activo', 'finalizado')."""
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Alquileres SET estado = ? WHERE id_alquiler = ?", (nuevo_estado, self.id_alquiler))
        conn.commit()
        conn.close()