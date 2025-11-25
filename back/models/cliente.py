import sqlite3
from database import Database
from services.alquiler_service import AlquilerService

class Cliente:
    def __init__(self, id_cliente, tipo_dni, dni, nombre, apellido, telefono, email, direccion, estado):
        self.id_cliente = id_cliente
        self.tipo_dni = tipo_dni
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.email = email
        self.direccion = direccion
        self.estado = estado

    def __repr__(self):
        return f"<Cliente {self.nombre} {self.apellido} (DNI: {self.dni})>"

    @staticmethod
    def create(tipo_dni, dni, nombre, apellido, telefono, email, direccion, estado="activo"):
        """Crea un nuevo cliente en la BD."""
        conn = Database().get_connection()
        cursor = conn.cursor()
        try:
            estado = estado or "activo"
            cursor.execute(
                "INSERT INTO Clientes (tipo_dni, dni, nombre, apellido, telefono, email, direccion, estado) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (tipo_dni, dni, nombre, apellido, telefono, email, direccion, estado)
            )
            conn.commit()
            return Cliente.get_by_id(cursor.lastrowid)
        except sqlite3.IntegrityError as e:
            print(f"Error al crear cliente: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_id(id_cliente):
        """Obtiene un cliente por su ID."""
        conn = Database().get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Clientes WHERE id_cliente = ?", (id_cliente,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Cliente(*row)
        return None
    
    @staticmethod
    def get_by_dni(dni):
        """Obtiene un cliente por su DNI."""
        conn = Database().get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Clientes WHERE dni = ?", (dni,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Cliente(*row)
        return None
    
    @staticmethod
    def get_all():
        """Obtiene todos los clientes."""
        conn = Database().get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Clientes")
        rows = cursor.fetchall()
        conn.close()
        return [Cliente(*row) for row in rows]

    @staticmethod
    def update(id_cliente, **fields):
        conn = Database().get_connection()
        cursor = conn.cursor()

        query_fields = [f"{k}=?" for k, v in fields.items() if v is not None]
        params = [v for v in fields.values() if v is not None]

        if not query_fields:
            return Cliente.get_by_id(id_cliente)

        params.append(id_cliente)

        try:
            cursor.execute(f"UPDATE Clientes SET {', '.join(query_fields)} WHERE id_cliente=?", params)
            conn.commit()
            return Cliente.get_by_id(id_cliente)
        except sqlite3.Error as e:
            conn.rollback()
            return None
        finally:
            conn.close()


    def is_available(self, fecha_inicio, fecha_fin):
        # Verfica si el cliente no tiene otro alquiler en las fechas futuras
        conn = Database().get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*) FROM Alquileres
            WHERE id_cliente = ?
            AND estado IN ('pendiente', 'confirmado')
            AND (
                (fecha_hora_inicio <= ? AND fecha_hora_fin_prevista >= ?)
                OR
                (fecha_hora_inicio <= ? AND fecha_hora_fin_prevista >= ?)
                OR
                (fecha_hora_inicio >= ? AND fecha_hora_fin_prevista <= ?)
            )
        """, (self.id_cliente, fecha_inicio, fecha_fin, fecha_inicio, fecha_fin, fecha_inicio, fecha_fin))
        count = cursor.fetchone()[0]
        conn.close()
        return count == 0
