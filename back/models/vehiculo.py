from datetime import datetime
import sqlite3
from database import Database
from services.mantenimiento_service import MantenimientoService

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
        conn = Database().get_connection()
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
            conn.rollback()
            return None
        finally:
            conn.close()

    @staticmethod
    def get_all():
        """Obtiene todos los vehículos."""
        conn = Database().get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Vehiculos")
        rows = cursor.fetchall()
        conn.close()
        return [Vehiculo(*row) for row in rows]

    @staticmethod
    def get_by_id(id_vehiculo):
        """Obtiene un vehículo por su ID."""
        conn = Database().get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Vehiculos WHERE id_vehiculo = ?", (id_vehiculo,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Vehiculo(*row)
        return None
        
    @staticmethod
    def get_by_patente(patente):
        conn = Database().get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Vehiculos WHERE patente = ?", (patente,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Vehiculo(*row)
        return None


    @staticmethod
    def update_estado(id_vehiculo, nuevo_estado):
        """Actualiza el estado del vehículo (ej. 'disponible', 'alquilado')."""
        conn = Database().get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Vehiculos SET estado = ? WHERE id_vehiculo = ?", (nuevo_estado, id_vehiculo))
        conn.commit()
        conn.close()
        print(f"Estado de vehículo {id_vehiculo} actualizado a: {nuevo_estado}")
        return Vehiculo.get_by_id(id_vehiculo)

    def is_available(self, fecha_inicio, fecha_fin, exclude_alquiler_id=None):
        """
        Verifica disponibilidad.
        :param exclude_alquiler_id: ID del alquiler actual (si estamos editando) para ignorarlo en el chequeo.
                                    Si es None o -1, se asume creación nueva.
        """
        # 1. Bloqueo físico
        if self.estado in ['mantenimiento', 'baja', 'inactivo', 'eliminado']:
            return False
            
        conn = Database().get_connection()
        cursor = conn.cursor()

        # Si no pasaron ID (es creación), usamos -1 para que la query SQL no falle
        id_a_excluir = exclude_alquiler_id if exclude_alquiler_id is not None else -1

        # 2. Chequear conflicto con Tabla ALQUILERES
        # (Excluyendo el alquiler propio con 'AND id_alquiler != ?')
        cursor.execute(
            """
            SELECT COUNT(*) FROM Alquileres
            WHERE id_vehiculo = ?
            AND id_alquiler != ?
            AND estado IN ('activo', 'pendiente') -- Chequeamos ambos estados activos
            AND (fecha_hora_inicio < ? AND fecha_hora_fin_prevista > ?)
            """,
            (self.id_vehiculo, id_a_excluir, fecha_fin, fecha_inicio)
        )
        alquileres_count = cursor.fetchone()[0]
        
        if alquileres_count > 0:
            print(f"Vehículo {self.patente} ocupado por {alquileres_count} alquiler(es).")
            conn.close()
            return False 

        conn.close()
        return alquileres_count == 0 



    @staticmethod
    def update(id_vehiculo, **fields):
        conn = Database().get_connection()
        cur = conn.cursor()

        query_fields = [f"{k}=?" for k, v in fields.items() if v is not None]
        params = [v for v in fields.values() if v is not None]

        if not query_fields:
            return Vehiculo.get_by_id(id_vehiculo)


        if 'mantenimiento' in fields.values():
            print("Poniendo vehículo en mantenimiento...")
            # Si se pone en mantenimiento, no se puede estar alquilado
            veh = Vehiculo.get_by_id(id_vehiculo)
            if veh and veh.estado in ['eliminado']:
                conn.close()
                return None
            
            man = MantenimientoService.get_active_by_vehiculo(id_vehiculo)
            if not man:
                fecha_hora_actual = datetime.now().isoformat(timespec='seconds')
                MantenimientoService.create({
                    "id_vehiculo": id_vehiculo,
                    "fecha_hora_inicio": fecha_hora_actual,
                    "descripcion": "Puesto en mantenimiento",
                    "costo": 1000
                })

        elif 'disponible' in fields.values():
            # Si se reactiva, cerrar mantenimiento activo
            mantenimientos = MantenimientoService.get_active_by_vehiculo(id_vehiculo)
            fecha_hora_actual = datetime.now().isoformat(timespec='seconds')
            if mantenimientos:
                MantenimientoService.update(mantenimientos.id_mantenimiento, {'fecha_hora_fin': fecha_hora_actual})
            

        params.append(id_vehiculo)
        
        try:
            print("Actualizando vehículo a", fields)
            cur.execute(f"UPDATE Vehiculos SET {', '.join(query_fields)} WHERE id_vehiculo=?", params)
            conn.commit()
            return Vehiculo.get_by_id(id_vehiculo)
        except:
            conn.rollback()
            return None
        finally:
            conn.close()


    @staticmethod
    def delete(id_vehiculo):
        conn = Database().get_connection()
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