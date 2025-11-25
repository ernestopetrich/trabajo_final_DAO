import sqlite3
from math import ceil 
from services.vehiculo_service import VehiculoService
from datetime import datetime, timedelta
from database import get_db_connection


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

    def eliminar(self):
        return self.state.eliminar(self)

    # --- MÉTODOS INTERNOS PARA EL STATE ---
    
    def set_estado(self, nuevo_estado_str):
        """
        Cambia el estado del objeto y lo persiste en la BD.
        Este método es llamado POR los objetos State.
        """
        self.estado_str = nuevo_estado_str # Actualizamos el string interno
        self.state = self._crear_estado(nuevo_estado_str) # Actualizamos el objeto State

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Alquileres SET estado = ? WHERE id_alquiler = ?", (nuevo_estado_str, self.id_alquiler))
        conn.commit()
        conn.close()

    def set_fecha_fin_real(self, fecha_iso):
        self.fecha_hora_fin_real = fecha_iso
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Alquileres SET fecha_hora_fin_real = ? WHERE id_alquiler = ?", (fecha_iso, self.id_alquiler))
        conn.commit()
        conn.close()

    def calcular_dias_alquiler(self):
        """Calcula la cantidad de días del alquiler."""
        inicio = datetime.fromisoformat(self.fecha_hora_inicio)
        
        if self.fecha_hora_fin_real:
            fin = datetime.fromisoformat(self.fecha_hora_fin_real)
        else:
            fin = datetime.now() 
        
        diferencia = fin - inicio
        dias_a_cobrar = ceil(diferencia.total_seconds() / 86400) 
        
        if dias_a_cobrar < 1:
            dias_a_cobrar = 1
            
        return dias_a_cobrar

    # --- CÁLCULO DE COSTOS (ACTUALIZADO CON MULTAS Y DAÑOS) ---
    def calcular_y_guardar_costo(self):
        """
        Calcula el costo total: (Días * Precio) + Multas + Daños.
        Se llama automáticamente desde el Estado al finalizar.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 1. Obtener precio diario del vehículo
        cursor.execute("SELECT precio_diario FROM Vehiculos WHERE id_vehiculo = ?", (self.id_vehiculo,))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            print("Error: No se encontró el vehículo para calcular costo.")
            return 0.0

        precio_diario = row['precio_diario']
        
        # 2. Calcular duración y costo base
        dias_a_cobrar = self.calcular_dias_alquiler()
            
        costo_base = dias_a_cobrar * precio_diario
        
        # 3. Sumar Multas
        # Usamos SUM(monto) para obtener el total de todas las multas de este alquiler
        cursor.execute("SELECT SUM(monto) FROM Multas WHERE id_alquiler = ?", (self.id_alquiler,))
        resultado_multas = cursor.fetchone()[0]
        total_multas = resultado_multas if resultado_multas else 0.0

        # 4. Sumar Daños
        # Usamos SUM(costo_reparacion) para obtener el total de reparaciones
        cursor.execute("SELECT SUM(costo_reparacion) FROM Danios WHERE id_alquiler = ?", (self.id_alquiler,))
        resultado_danios = cursor.fetchone()[0]
        total_danios = resultado_danios if resultado_danios else 0.0

        # 5. Calcular Total Final
        monto_total = costo_base + total_multas + total_danios
        
        # 6. Actualizar objeto y BD
        self.costo_total = monto_total
        cursor.execute("UPDATE Alquileres SET costo_total = ? WHERE id_alquiler = ?", (monto_total, self.id_alquiler))
        conn.commit()
        conn.close()
        
        # Log detallado para control
        print(f"--- Cierre de Alquiler #{self.id_alquiler} ---")
        print(f"Costo Base ({dias_a_cobrar} días): ${costo_base}")
        print(f"Multas: ${total_multas}")
        print(f"Daños: ${total_danios}")
        print(f"TOTAL FINAL: ${monto_total}")
        
        return monto_total


    # --- MÉTODOS ESTÁTICOS (CRUD) ---
    @staticmethod
    def create(id_cliente, id_vehiculo, id_empleado, fecha_hora_inicio, fecha_hora_fin_prevista):
        conn = get_db_connection()
        cursor = conn.cursor()
        try:

            estado_inicial = 'pendiente' 
            
            vehiculo = VehiculoService.get_by_id(id_vehiculo)

            if vehiculo.is_available(fecha_hora_inicio, fecha_hora_fin_prevista) == False:
                print("Error: El vehículo no está disponible en las fechas solicitadas.")
                return 'Vehiculo: {vehiculo.patente} No disponible'

            cursor.execute(
                "INSERT INTO Alquileres (id_cliente, id_vehiculo, id_empleado, fecha_hora_inicio, fecha_hora_fin_prevista, estado) VALUES (?, ?, ?, ?, ?, ?)",
                (id_cliente, id_vehiculo, id_empleado, fecha_hora_inicio, fecha_hora_fin_prevista, estado_inicial)
            )
            id_alquiler = cursor.lastrowid
            conn.commit()
            return Alquiler.get_by_id(id_alquiler)
        except sqlite3.Error as e:
            print(f"Error al crear alquiler: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()

    @staticmethod
    def create_raw(id_cliente, id_vehiculo, id_empleado,
                fecha_inicio, fecha_fin_prevista,
                estado="pendiente",
                fecha_fin_real=None,
                costo_total=None):
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO Alquileres
                (id_cliente, id_vehiculo, id_empleado,
                fecha_hora_inicio, fecha_hora_fin_prevista,
                fecha_hora_fin_real, costo_total, estado)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                id_cliente,
                id_vehiculo,
                id_empleado,
                fecha_inicio,
                fecha_fin_prevista,
                fecha_fin_real,
                costo_total,
                estado
            ))

            conn.commit()
            return Alquiler.get_by_id(cursor.lastrowid)

        except Exception as e:
            print("ERROR create_raw:", e)
            conn.rollback()
            return None
        finally:
            conn.close()


    @staticmethod
    def get_by_id(id_alquiler):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Alquileres WHERE id_alquiler = ?", (id_alquiler,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Alquiler(*row)
        return None
    
    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Alquileres")
        rows = cursor.fetchall()
        conn.close()
        return [Alquiler(*row) for row in rows]

    @staticmethod
    def update(id_alquiler, **fields):
        """Actualiza cualquier campo del alquiler."""
        conn = get_db_connection()
        cursor = conn.cursor()

        if 'estado' in fields:
            del fields['estado']  # El estado se maneja por los métodos del State
            print(f"ADVERTENCIA: Se intentó actualizar 'estado' directamente en Alquiler #{id_alquiler}. El campo será ignorado.")

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

        except sqlite3.Error as e:
            print(f"Error al actualizar alquiler: {e}")
            conn.rollback()
        finally:
            conn.close()

        return Alquiler.get_by_id(id_alquiler)
