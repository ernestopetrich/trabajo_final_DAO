import sqlite3
import database

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
    def create(tipo_dni, dni, nombre, apellido, telefono, email, direccion):
        """Crea un nuevo cliente en la BD."""
        conn = database.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO Clientes (tipo_dni, dni, nombre, apellido, telefono, email, direccion) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (tipo_dni, dni, nombre, apellido, telefono, email, direccion)
            )
            conn.commit()
            return Cliente.get_by_id(cursor.lastrowid)
        except sqlite3.IntegrityError as e:
            print(f"Error al crear cliente: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_id(id_cliente):
        """Obtiene un cliente por su ID."""
        conn = database.get_db_connection()
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
        conn = database.get_db_connection()
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
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Clientes")
        rows = cursor.fetchall()
        conn.close()
        return [Cliente(*row) for row in rows]

    @staticmethod
    def update(id_cliente, **fields):
        conn = database.get_db_connection()
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
        except:
            conn.rollback()
            return None
        finally:
            conn.close()

