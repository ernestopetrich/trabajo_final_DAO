import sqlite3
import database

class Cliente:
    def __init__(self, id_cliente, tipo_dni, dni, nombre, apellido, telefono, email, direccion):
        self.id_cliente = id_cliente
        self.tipo_dni = tipo_dni
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.email = email
        self.direccion = direccion

    @staticmethod
    def create(tipo_dni, dni, nombre, apellido, telefono, email, direccion):
        conn = database.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO Clientes (tipo_dni, dni, nombre, apellido, telefono, email, direccion)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (tipo_dni, dni, nombre, apellido, telefono, email, direccion))
            conn.commit()
            return Cliente.get_by_id(cursor.lastrowid)
        except sqlite3.IntegrityError:
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_id(id_cliente):
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Clientes WHERE id_cliente=?", (id_cliente,))
        row = cursor.fetchone()
        conn.close()
        return Cliente(*row) if row else None

    @staticmethod
    def get_by_dni(dni):
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Clientes WHERE dni=?", (dni,))
        row = cursor.fetchone()
        conn.close()
        return Cliente(*row) if row else None

    @staticmethod
    def get_all():
        conn = database.get_db_connection()
        cursor = conn.cursor()
        print("Error 3")
        cursor.execute("SELECT * FROM Clientes")
        print("Error 4")
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

    @staticmethod
    def delete(id_cliente):
        conn = database.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM Clientes WHERE id_cliente=?", (id_cliente,))
            conn.commit()
            return cursor.rowcount > 0
        except:
            conn.rollback()
            return False
        finally:
            conn.close()
