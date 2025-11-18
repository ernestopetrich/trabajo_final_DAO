import sqlite3
import database

class Reserva:
    def __init__(self, id_reserva, id_cliente, id_vehiculo, fecha_inicio, fecha_fin, estado):
        self.id_reserva = id_reserva
        self.id_cliente = id_cliente
        self.id_vehiculo = id_vehiculo
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.estado = estado
    
    def __repr__(self):
        return f"<Reserva #{self.id_reserva} (Veh: {self.id_vehiculo}) {self.fecha_inicio} a {self.fecha_fin} - {self.estado}>"

    @staticmethod
    def create(id_cliente, id_vehiculo, fecha_inicio, fecha_fin, estado='pendiente'):
        """Crea una nueva reserva."""
        conn = database.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO Reservas (id_cliente, id_vehiculo, fecha_inicio, fecha_fin, estado) VALUES (?, ?, ?, ?, ?)",
                (id_cliente, id_vehiculo, fecha_inicio, fecha_fin, estado)
            )
            conn.commit()
            return Reserva.get_by_id(cursor.lastrowid)
        except sqlite3.Error as e:
            print(f"Error al crear reserva: {e}")
            return None
        finally:
            conn.close()
    
    @staticmethod
    def get_by_id(id_reserva):
        """Obtiene una reserva por su ID."""
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Reservas WHERE id_reserva = ?", (id_reserva,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Reserva(*row)
        return None
    
    @staticmethod
    def get_all():
        """Obtiene todas las reservas."""
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Reservas")
        rows = cursor.fetchall()
        conn.close()
        return [Reserva(*row) for row in rows]

    def update_estado(self, nuevo_estado):
        """Actualiza el estado de la reserva (ej. 'confirmada', 'cancelada')."""
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Reservas SET estado = ? WHERE id_reserva = ?", (nuevo_estado, self.id_reserva))
        conn.commit()
        conn.close()
        self.estado = nuevo_estado
        print(f"Reserva #{self.id_reserva} actualizada a: {nuevo_estado}")

    def delete(self):
        """Elimina la reserva de la base de datos."""
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Reservas WHERE id_reserva = ?", (self.id_reserva,))
        conn.commit()
        conn.close()
        print(f"Reserva #{self.id_reserva} eliminada de la base de datos.")

