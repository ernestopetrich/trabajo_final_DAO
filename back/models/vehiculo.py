import sqlite3
import database

class Vehiculo:
    def __init__(self, id_vehiculo, marca, modelo, anio, tipo, patente, kilometraje, estado):
        self.id_vehiculo = id_vehiculo
        self.marca = marca
        self.modelo = modelo
        self.anio = anio
        self.tipo = tipo
        self.patente = patente
        self.kilometraje = kilometraje
        self.estado = estado

    @staticmethod
    def create(marca, modelo, anio, tipo, patente, kilometraje, estado):
        conn = database.get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO Vehiculos (marca, modelo, anio, tipo, patente, kilometraje, estado)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (marca, modelo, anio, tipo, patente, kilometraje, estado))
            conn.commit()
            return Vehiculo.get_by_id(cur.lastrowid)
        except sqlite3.IntegrityError:
            return None
        finally:
            conn.close()

    @staticmethod
    def get_all():
        conn = database.get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Vehiculos")
        rows = cur.fetchall()
        conn.close()
        return [Vehiculo(*row) for row in rows]

    @staticmethod
    def get_by_id(id_vehiculo):
        conn = database.get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Vehiculos WHERE id_vehiculo=?", (id_vehiculo,))
        row = cur.fetchone()
        conn.close()
        return Vehiculo(*row) if row else None

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
