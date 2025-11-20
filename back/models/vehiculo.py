import sqlite3
import database

class Vehiculo:
    def __init__(self, id_vehiculo, patente, marca, modelo, nombre, precio_diario, estado):
        self.id_vehiculo = id_vehiculo
        self.patente = patente
        self.marca = marca
        self.modelo = modelo
        self.nombre = nombre
        self.precio_diario = precio_diario
        self.estado = estado

    def __repr__(self):
        return f"<Vehiculo {self.marca} {self.modelo} (Patente: {self.patente}) - {self.estado}>"

    @staticmethod
    def create(patente, marca, modelo, nombre, precio_diario, estado='disponible'):
        """Crea un nuevo vehículo."""
        conn = database.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO Vehiculos (patente, marca, modelo, nombre, precio_diario, estado) VALUES (?, ?, ?, ?, ?, ?)",
                (patente, marca, modelo, nombre, precio_diario, estado)
            )
            conn.commit()
            return Vehiculo.get_by_id(cursor.lastrowid)
        except sqlite3.IntegrityError as e:
            print(f"Error al crear vehículo: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_all():
        """Obtiene todos los vehículos."""
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Vehiculos")
        rows = cursor.fetchall()
        conn.close()
        return [Vehiculo(*row) for row in rows]

    @staticmethod
    def get_by_id(id_vehiculo):
        """Obtiene un vehículo por su ID."""
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Vehiculos WHERE id_vehiculo = ?", (id_vehiculo,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Vehiculo(*row)
        return None

    def update_estado(self, nuevo_estado):
        """Actualiza el estado del vehículo (ej. 'disponible', 'alquilado')."""
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Vehiculos SET estado = ? WHERE id_vehiculo = ?", (nuevo_estado, self.id_vehiculo))
        conn.commit()
        conn.close()
        self.estado = nuevo_estado
        print(f"Estado de {self.patente} actualizado a: {nuevo_estado}")

    def is_available(self, fecha_inicio, fecha_fin):
        """
        Verifica la disponibilidad del vehículo en un rango de fechas.
        Debe chequear contra Alquileres activos y Reservas confirmadas.
        Esta es la lógica clave de tu sistema.
        """
        if self.estado != 'disponible':
            return False
            
        conn = database.get_db_connection()
        cursor = conn.cursor()

        # 1. Chequear contra Alquileres activos (que no estén finalizados o cancelados)
        # Un vehículo está ocupado si un alquiler existente se solapa con las fechas solicitadas.
        # Solapamiento: (InicioAlquiler < FinSolicitud) AND (FinAlquiler > InicioSolicitud)
        cursor.execute(
            """
            SELECT COUNT(*) FROM Alquileres
            WHERE id_vehiculo = ?
            AND estado = 'activo'
            AND (
                (fecha_hora_inicio < ? AND fecha_hora_fin_prevista > ?) OR -- Se solapa
                (fecha_hora_inicio BETWEEN ? AND ?) OR -- Comienza dentro
                (fecha_hora_fin_prevista BETWEEN ? AND ?) -- Termina dentro
            )
            """,
            (self.id_vehiculo, fecha_fin, fecha_inicio, fecha_inicio, fecha_fin, fecha_inicio, fecha_fin)
        )
        alquileres_count = cursor.fetchone()[0]
        print("cantidad de alquileres del vehiculo",alquileres_count)
        if alquileres_count > 0:
            conn.close()
            return False # Ocupado por un alquiler

        # 2. Chequear contra Reservas (que estén pendientes o confirmadas)
        cursor.execute(
            """
            SELECT COUNT(*) FROM Reservas
            WHERE id_vehiculo = ?
            AND (estado = 'pendiente' OR estado = 'confirmada')
            AND (
                (fecha_inicio < ? AND fecha_fin > ?) OR
                (fecha_inicio BETWEEN ? AND ?) OR
                (fecha_fin BETWEEN ? AND ?)
            )
            """,
            (self.id_vehiculo, fecha_fin, fecha_inicio, fecha_inicio, fecha_fin, fecha_inicio, fecha_fin)
        )
        reservas_count = cursor.fetchone()[0]
        print("cantidad de reservas del vehiculo", reservas_count)
        conn.close()
        return reservas_count == 0 # True si no hay alquileres NI reservas


    @staticmethod
    def update(id_vehiculo, **fields):
        conn = database.get_db_connection()
        cur = conn.cursor()

        query_fields = [f"{k}=?" for k, v in fields.items() if v is not None]
        params = [v for v in fields.values() if v is not None]

        if not query_fields:
            return Vehiculo.get_by_id(id_vehiculo)

        params.append(id_vehiculo)

        try:
            cur.execute(f"UPDATE Vehiculos SET {', '.join(query_fields)} WHERE id_vehiculo=?", params)
            conn.commit()
            return Vehiculo.get_by_id(id_vehiculo)
        except:
            conn.rollback()
            return None
        finally:
            conn.close()

    @staticmethod
    def update_estado(id_vehiculo, nuevo_estado):
        conn = database.get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("UPDATE Vehiculos SET estado = ? WHERE id_vehiculo=?", (nuevo_estado, id_vehiculo))
            conn.commit()
            return True
        except:
            conn.rollback()
            return False
        finally:
            conn.close()

    @staticmethod
    def delete(id_vehiculo):
        conn = database.get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM Vehiculos WHERE id_vehiculo=?", (id_vehiculo,))
            conn.commit()
            return cur.rowcount > 0
        except:
            conn.rollback()
            return False
        finally:
            conn.close()
