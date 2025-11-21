import sqlite3
import database
from datetime import datetime, timedelta
from models.state_alquiler import EstadoActivo, EstadoFinalizado

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
        self.state = self._crear_estado(self.estado)

    def __repr__(self):
        return f"<Alquiler #{self.id_alquiler} (Veh: {self.id_vehiculo}) - {self.estado}>"
    
    def _crear_estado(self, estado):
        if estado == "activo":
            return EstadoActivo()
        elif estado == "finalizado":
            return EstadoFinalizado()
        else:
            return EstadoActivo()
        
    def set_estado(self, nuevo_estado):
        self.estado = nuevo_estado
        self.state = self._crear_estado(nuevo_estado)

        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Alquileres SET estado = ? WHERE id_alquiler = ?", (nuevo_estado, self.id_alquiler))
        conn.commit()
        conn.close()

    def set_fecha_fin_real(self, fecha_iso):
        self.fecha_hora_fin_real = fecha_iso

        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Alquileres SET fecha_hora_fin_real = ? WHERE id_alquiler = ?", (fecha_iso, self.id_alquiler))
        conn.commit()
        conn.close()

    @staticmethod
    def create(id_cliente, id_vehiculo, id_empleado, fecha_hora_inicio, fecha_hora_fin_prevista):
        """Crea un nuevo alquiler y marca el vehículo como 'alquilado'."""

        # Convertir a datetime
        inicio = datetime.fromisoformat(fecha_hora_inicio)
        fin_prevista = datetime.fromisoformat(fecha_hora_fin_prevista)
        ahora = datetime.now()

        # 1) Validar que inicio sea >= ahora
        if inicio < ahora:
            print(" La fecha de inicio no puede ser menor a la fecha y hora actual.")
            return None

        # 2) Validar que fin prevista sea mínimo +1 hora
        if fin_prevista < inicio + timedelta(hours=1):
            print(" La fecha/hora fin prevista debe ser mínimo 1 hora después del inicio.")
            return None
        # 3) Crear alquiler y actualizar estado del vehículo
        conn = database.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO Alquileres (id_cliente, id_vehiculo, id_empleado, fecha_hora_inicio, fecha_hora_fin_prevista, estado) VALUES (?, ?, ?, ?, ?, ?)",
                (id_cliente, id_vehiculo, id_empleado, fecha_hora_inicio, fecha_hora_fin_prevista, 'activo')
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

        def devolver(self):
            return self.state.devolver(self)


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
    
