import sqlite3
import database
from datetime import datetime, timedelta
# Importamos todas las clases de estado
from models.state_alquiler import (
    EstadoPendiente, 
    EstadoConfirmado, 
    EstadoActivo, 
    EstadoFinalizado,
    EstadoCancelado
)

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
        
        # Inicialización del State
        self.estado_str = estado # Guardamos el string original internamente
        self.state = self._crear_estado(estado)

    # --- CORRECCIÓN CLAVE ---
    @property
    def estado(self):
        """
        Propiedad para que Pydantic (la API) pueda leer 'alquiler.estado'.
        Devuelve el string del estado actual.
        """
        return self.estado_str

    def __repr__(self):
        return f"<Alquiler #{self.id_alquiler} - Estado: {self.estado_str}>"
    
    # --- FACTORY DE ESTADOS ---
    def _crear_estado(self, estado_db):
        """Convierte el string de la BD en un objeto Estado."""
        estado_db = estado_db.lower()
        if estado_db == "pendiente":
            return EstadoPendiente()
        elif estado_db == "confirmado":
            return EstadoConfirmado()
        elif estado_db == "activo":
            return EstadoActivo()
        elif estado_db == "finalizado":
            return EstadoFinalizado()
        elif estado_db == "cancelado" or estado_db == "eliminado":
            return EstadoCancelado()
        else:
            print(f"Advertencia: Estado desconocido '{estado_db}', se tratará como Finalizado.")
            return EstadoFinalizado()

    # --- MÉTODOS DEL CONTEXTO (DELEGACIÓN) ---
    def confirmar(self):
        return self.state.confirmar(self)

    def iniciar(self):
        return self.state.iniciar(self)

    def devolver(self):
        return self.state.devolver(self)

    def cancelar(self):
        return self.state.cancelar(self)

    # --- MÉTODOS INTERNOS PARA EL STATE ---
    
    def set_estado(self, nuevo_estado_str):
        """
        Cambia el estado del objeto y lo persiste en la BD.
        Este método es llamado POR los objetos State.
        """
        self.estado_str = nuevo_estado_str # Actualizamos el string interno
        self.state = self._crear_estado(nuevo_estado_str) # Actualizamos el objeto State

        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Alquileres SET estado = ? WHERE id_alquiler = ?", (nuevo_estado_str, self.id_alquiler))
        conn.commit()
        conn.close()

    def set_fecha_fin_real(self, fecha_iso):
        self.fecha_hora_fin_real = fecha_iso
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Alquileres SET fecha_hora_fin_real = ? WHERE id_alquiler = ?", (fecha_iso, self.id_alquiler))
        conn.commit()
        conn.close()

    # --- MÉTODOS ESTÁTICOS (CRUD) ---
    @staticmethod
    def create(id_cliente, id_vehiculo, id_empleado, fecha_hora_inicio, fecha_hora_fin_prevista):
        conn = database.get_db_connection()
        cursor = conn.cursor()
        try:
            estado_inicial = 'activo' 
            
            cursor.execute(
                "INSERT INTO Alquileres (id_cliente, id_vehiculo, id_empleado, fecha_hora_inicio, fecha_hora_fin_prevista, estado) VALUES (?, ?, ?, ?, ?, ?)",
                (id_cliente, id_vehiculo, id_empleado, fecha_hora_inicio, fecha_hora_fin_prevista, estado_inicial)
            )
            id_alquiler = cursor.lastrowid
            
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

    @staticmethod
    def update(id_alquiler, **fields):
        """Actualiza cualquier campo del alquiler."""
        conn = database.get_db_connection()
        cursor = conn.cursor()

        # Filtrar campos válidos (evita columnas inexistentes)
        valid_fields = {k: v for k, v in fields.items() if v is not None}

        if not valid_fields:
            conn.close()
            return Alquiler.get_by_id(id_alquiler)

        query_fields = [f"{k}=?" for k in valid_fields.keys()]
        params = list(valid_fields.values())
        params.append(id_alquiler)

        try:
            cursor.execute(
                f"UPDATE Alquileres SET {', '.join(query_fields)} WHERE id_alquiler=?",
                params
            )
            conn.commit()
        finally:
            conn.close()

        return Alquiler.get_by_id(id_alquiler)



    def calcular_monto(self):
        """Calcula el monto total del alquiler basado en la duración y el precio diario del vehículo."""
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT precio_diario FROM Vehiculos WHERE id_vehiculo = ?", (self.id_vehiculo,))
        row = cursor.fetchone()
        conn.close()
        if row:
            precio_diario = row[0]
            from datetime import datetime
            fecha_inicio = datetime.fromisoformat(self.fecha_hora_inicio)
            fecha_fin = datetime.fromisoformat(self.fecha_hora_fin_prevista)
            dias_alquiler = (fecha_fin - fecha_inicio).days + 1  # Incluir el día de inicio
            return dias_alquiler * precio_diario
        return 0
    
