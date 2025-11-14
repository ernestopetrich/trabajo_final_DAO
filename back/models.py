from math import ceil
import database
import sqlite3 # Importar sqlite3 para manejar IntegrityError
from datetime import datetime
from utils import to_iso


# Usamos un patrón simple donde las clases tienen métodos estáticos
# para interactuar con la BD. Una instancia de la clase representa
# un registro específico (un "modelo").

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
    def update(id_cliente, tipo_dni=None, dni=None, nombre=None, apellido=None, telefono=None, email=None, direccion=None):
        fields = []
        params = []
        mapping = {
            "tipo_dni": tipo_dni, "dni": dni, "nombre": nombre, "apellido": apellido,
            "telefono": telefono, "email": email, "direccion": direccion
        }
        for k, v in mapping.items():
            if v is not None:
                fields.append(f"{k} = ?")
                params.append(v)
        if not fields:
            return Cliente.get_by_id(id_cliente)  # nada para actualizar

        params.append(id_cliente)
        conn = database.get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(f"UPDATE Clientes SET {', '.join(fields)} WHERE id_cliente = ?", params)
            conn.commit()
            return Cliente.get_by_id(id_cliente)
        except Exception as e:
            print("Error updating cliente:", e)
            conn.rollback()
            return None
        finally:
            conn.close()

    @staticmethod
    def delete(id_cliente):
        conn = database.get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM Clientes WHERE id_cliente = ?", (id_cliente,))
            conn.commit()
            return cur.rowcount > 0
        except Exception as e:
            print("Error deleting cliente:", e)
            conn.rollback()
            return False
        finally:
            conn.close()

class Empleado:
    def __init__(self, id_empleado, tipo_dni, dni, nombre, apellido):
        self.id_empleado = id_empleado
        self.tipo_dni = tipo_dni
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido

    def __repr__(self):
        return f"<Empleado {self.nombre} {self.apellido} (DNI: {self.dni})>"

    @staticmethod
    def create(tipo_dni, dni, nombre, apellido):
        """Crea un nuevo empleado en la BD."""
        conn = database.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO Empleados (tipo_dni, dni, nombre, apellido) VALUES (?, ?, ?, ?)",
                (tipo_dni, dni, nombre, apellido)
            )
            conn.commit()
            return Empleado.get_by_id(cursor.lastrowid)
        except sqlite3.IntegrityError as e:
            print(f"Error al crear empleado: {e}")
            return None
        finally:
            conn.close()
        
    @staticmethod
    def get_all():
        """Obtiene todos los empleados."""
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Empleados")
        rows = cursor.fetchall()
        conn.close()
        return [Empleado(*row) for row in rows]

    @staticmethod
    def get_by_id(id_empleado):
        """Obtiene un empleado por su ID."""
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Empleados WHERE id_empleado = ?", (id_empleado,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Empleado(*row)
        return None
    
    @staticmethod
    def get_by_dni(dni):
        """Obtiene un empleado por su DNI."""
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Empleados WHERE dni = ?", (dni,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Empleado(*row)
        return None

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
    
    @staticmethod
    def update(id_vehiculo, patente=None, marca=None, modelo=None, nombre=None, precio_diario=None, estado=None):
        fields = []
        params = []
        mapping = {
            "patente": patente, "marca": marca, "modelo": modelo, "nombre": nombre,
            "precio_diario": precio_diario, "estado": estado
        }
        for k, v in mapping.items():
            if v is not None:
                fields.append(f"{k} = ?")
                params.append(v)
        if not fields:
            return Vehiculo.get_by_id(id_vehiculo)

        params.append(id_vehiculo)
        conn = database.get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(f"UPDATE Vehiculos SET {', '.join(fields)} WHERE id_vehiculo = ?", params)
            conn.commit()
            return Vehiculo.get_by_id(id_vehiculo)
        except Exception as e:
            print("Error updating vehiculo:", e)
            conn.rollback()
            return None
        finally:
            conn.close()

    @staticmethod
    def delete(id_vehiculo):
        conn = database.get_db_connection()
        cur = conn.cursor()
        try:
            # opcional: impedir borrado si está alquilado
            cur.execute("SELECT estado FROM Vehiculos WHERE id_vehiculo = ?", (id_vehiculo,))
            r = cur.fetchone()
            if r and r[0] == 'alquilado':
                print("No se puede borrar un vehículo alquilado.")
                return False
            cur.execute("DELETE FROM Vehiculos WHERE id_vehiculo = ?", (id_vehiculo,))
            conn.commit()
            return cur.rowcount > 0
        except Exception as e:
            print("Error deleting vehiculo:", e)
            conn.rollback()
            return False
        finally:
            conn.close()

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


class Alquiler:
    def __init__(self, id_alquiler, id_cliente, id_vehiculo, id_empleado, fecha_hora_inicio, fecha_hora_fin_prevista, fecha_hora_fin_real, costo_total, estado):
        self.id_alquiler = id_alquiler
        self.id_cliente = id_cliente
        self.id_vehiculo = id_vehiculo
        self.id_empleado = id_empleado
        self.fecha_hora_inicio = to_iso(fecha_hora_inicio)
        self.fecha_hora_fin_prevista = to_iso(fecha_hora_fin_prevista)
        self.fecha_hora_fin_real = to_iso(fecha_hora_fin_real)
        self.costo_total = costo_total
        self.estado = estado

    def __repr__(self):
        return f"<Alquiler #{self.id_alquiler} (Veh: {self.id_vehiculo}) - {self.estado}>"

    @staticmethod
    def create(id_cliente, id_vehiculo, id_empleado, fecha_hora_inicio, fecha_hora_fin_prevista):
        """Crea un nuevo alquiler y marca el vehículo como 'alquilado'."""
        
        # 1. Crear el registro de alquiler
        conn = database.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO Alquileres (id_cliente, id_vehiculo, id_empleado, fecha_hora_inicio, fecha_hora_fin_prevista, estado) VALUES (?, ?, ?, ?, ?, ?)",
                (id_cliente, id_vehiculo, id_empleado, fecha_hora_inicio, fecha_hora_fin_prevista, 'activo')
            )
            id_alquiler = cursor.lastrowid
            
            # 2. Actualizar estado del vehículo
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
        conn = database.get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Alquileres")
        rows = cur.fetchall()
        conn.close()
        return [Alquiler(*row) for row in rows]

    def devolver(self):
        """Marca el alquiler como finalizado, calcula costo_total y libera el vehículo."""
        # self is an instance (Alquiler)
        if self.estado != 'activo':
            print(f"Alquiler #{self.id_alquiler} no está activo. No se puede devolver.")
            return False

        # Parse dates robustamente (intentar varios formatos)
        def parse_dt(s):
            fmts = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%d/%m/%Y %H:%M:%S", "%d/%m/%Y"]
            for f in fmts:
                try:
                    return datetime.strptime(s, f)
                except Exception:
                    continue
            raise ValueError(f"No se pudo parsear la fecha: {s}")

        try:
            inicio_dt = parse_dt(self.fecha_hora_inicio)
        except Exception as e:
            print("Error parse inicio:", e)
            return False

        now_dt = datetime.now()
        dias = max(1, ceil((now_dt - inicio_dt).total_seconds() / 86400))
        # obtener precio diario del vehiculo
        veh = Vehiculo.get_by_id(self.id_vehiculo)
        if not veh:
            print("Vehículo no encontrado al devolver.")
            return False
        precio_diario = float(veh.precio_diario)

        costo = dias * precio_diario

        conn = database.get_db_connection()
        cur = conn.cursor()
        try:
            fecha_fin_real_str = now_dt.strftime("%Y-%m-%d %H:%M:%S")
            cur.execute(
                "UPDATE Alquileres SET fecha_hora_fin_real = ?, costo_total = ?, estado = ? WHERE id_alquiler = ?",
                (fecha_fin_real_str, costo, 'finalizado', self.id_alquiler)
            )
            cur.execute("UPDATE Vehiculos SET estado = 'disponible' WHERE id_vehiculo = ?", (self.id_vehiculo,))
            conn.commit()

            # actualizar atributos del objeto en memoria
            self.fecha_hora_fin_real = fecha_fin_real_str
            self.costo_total = costo
            self.estado = 'finalizado'
            print(f"Alquiler #{self.id_alquiler} devuelto. Costo: {costo}, días: {dias}")
            return True
        except Exception as e:
            print("Error al devolver alquiler:", e)
            conn.rollback()
            return False
        finally:
            conn.close()


# Puedes seguir añadiendo las clases para Empleado, Mantenimiento, Multa, Danio, etc.
# siguiendo el mismo patrón.


class Mantenimiento:
    def __init__(self, id_mantenimiento, id_vehiculo, fecha_hora_inicio, fecha_hora_fin, descripcion, costo):
        self.id_mantenimiento = id_mantenimiento
        self.id_vehiculo = id_vehiculo
        self.fecha_hora_inicio = to_iso(fecha_hora_inicio)
        self.fecha_hora_fin = to_iso(fecha_hora_fin)
        self.descripcion = descripcion
        self.costo = costo

    def __repr__(self):
        return f"<Mantenimiento #{self.id_mantenimiento} (Veh: {self.id_vehiculo}) - {self.estado}>"
    
    @staticmethod
    def create(id_vehiculo, fecha_hora_inicio, fecha_hora_fin, descripcion, costo):
        """Crea un nuevo registro de mantenimiento."""
        conn = database.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO Mantenimientos (id_vehiculo, fecha_hora_inicio, fecha_hora_fin, descripcion, costo) VALUES (?, ?, ?, ?, ?)",
                (id_vehiculo, fecha_hora_inicio, fecha_hora_fin, descripcion, costo)
            )
            conn.commit()
            return Mantenimiento.get_by_id(cursor.lastrowid)
        except sqlite3.Error as e:
            print(f"Error al crear mantenimiento: {e}")
            return None
        finally:
            conn.close()
        
    @staticmethod
    def get_by_id(id_mantenimiento):
        """Obtiene un mantenimiento por su ID."""
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Mantenimientos WHERE id_mantenimiento = ?", (id_mantenimiento,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Mantenimiento(*row)
        return None
    
    @staticmethod
    def get_all():
        """Obtiene todos los mantenimientos."""
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Mantenimientos")
        rows = cursor.fetchall()
        conn.close()
        return [Mantenimiento(*row) for row in rows]
    


class Multa:
    def __init__(self, id_multa, id_alquiler, descripcion, monto, fecha_hora_multa, estado):
        self.id_multa = id_multa
        self.id_alquiler = id_alquiler
        self.descripcion = descripcion
        self.monto = monto
        self.fecha_hora_multa = to_iso(fecha_hora_multa)
        self.estado = estado
    
    def __repr__(self):
        return f"<Multa #{self.id_multa} (Alquiler: {self.id_alquiler}) - {self.estado}>"
    
    @staticmethod
    def create(id_alquiler, descripcion, monto, fecha_hora_multa, estado='pendiente'):
        """Crea una nueva multa."""
        conn = database.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO Multas (id_alquiler, descripcion, monto, fecha_hora_multa, estado) VALUES (?, ?, ?, ?, ?)",
                (id_alquiler, descripcion, monto, fecha_hora_multa, estado)
            )
            conn.commit()
            return Multa.get_by_id(cursor.lastrowid)
        except sqlite3.Error as e:
            print(f"Error al crear multa: {e}")
            return None
        finally:
            conn.close()
    
    @staticmethod
    def get_by_id_alquiler(id_alquiler):
        """Obtiene una multa por su ID de alquiler."""
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Multas WHERE id_alquiler = ?", (id_alquiler,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Multa(*row)
        return None
    
    @staticmethod
    def get_all():
        """Obtiene todas las multas."""
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Multas")
        rows = cursor.fetchall()
        conn.close()
        return [Multa(*row) for row in rows]
    


class Danio:
    def __init__(self, id_danio, id_alquiler, descripcion, costo_reparacion, fecha_hora_reporte, estado):
        self.id_danio = id_danio
        self.id_alquiler = id_alquiler
        self.descripcion = descripcion
        self.costo_reparacion = costo_reparacion
        self.fecha_hora_reporte = to_iso(fecha_hora_reporte)
        self.estado = estado

    def __repr__(self):
        return f"<Danio #{self.id_danio} (Alquiler: {self.id_alquiler}) - {self.estado}>"
    
    @staticmethod
    def create(id_alquiler, descripcion, costo_reparacion, fecha_hora_reporte, estado='pendiente'):
        """Crea un nuevo daño."""
        conn = database.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO Danios (id_alquiler, descripcion, costo_reparacion, fecha_hora_reporte, estado) VALUES (?, ?, ?, ?, ?)",
                (id_alquiler, descripcion, costo_reparacion, fecha_hora_reporte, estado)
            )
            conn.commit()
            return Danio.get_by_id(cursor.lastrowid)
        except sqlite3.Error as e:
            print(f"Error al crear daño: {e}")
            return None
        finally:
            conn.close()
        
    @staticmethod
    def get_by_id_alquiler(id_alquiler):
        """Obtiene un daño por su ID de alquiler."""
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Danios WHERE id_alquiler = ?", (id_alquiler,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Danio(*row)
        return None
    
    @staticmethod
    def get_all():
        """Obtiene todos los daños."""
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Danios")
        rows = cursor.fetchall()
        conn.close()
        return [Danio(*row) for row in rows]
    

class Factura:
    def __init__(self, id_factura, id_alquiler, fecha_hora_emision, monto_total, estado_pago):
        self.id_factura = id_factura
        self.id_alquiler = id_alquiler
        self.fecha_hora_emision = to_iso(fecha_hora_emision)
        self.monto_total = monto_total
        self.estado_pago = estado_pago

    def __repr__(self):
        return f"<Factura #{self.id_factura} (Alquiler: {self.id_alquiler}) - {self.estado_pago}>"
    
    @staticmethod
    def create(id_alquiler, fecha_hora_emision, monto_total, estado_pago='pendiente'):
        """Crea una nueva factura."""
        conn = database.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO Facturas (id_alquiler, fecha_hora_emision, monto_total, estado_pago) VALUES (?, ?, ?, ?)",
                (id_alquiler, fecha_hora_emision, monto_total, estado_pago)
            )
            conn.commit()
            return Factura.get_by_id(cursor.lastrowid)
        except sqlite3.Error as e:
            print(f"Error al crear factura: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_id(id_factura):
        """Obtiene una factura por su ID."""
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Facturas WHERE id_factura = ?", (id_factura,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Factura(*row)
        return None

    @staticmethod
    def get_all():
        """Obtiene todas las facturas."""
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Facturas")
        rows = cursor.fetchall()
        conn.close()
        return [Factura(*row) for row in rows]
    

class DetalleFactura:
    def __init__(self, id_detalle, id_factura, descripcion, cantidad, precio_unitario):
        self.id_detalle = id_detalle
        self.id_factura = id_factura
        self.descripcion = descripcion
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario

    def __repr__(self):
        return f"<DetalleFactura #{self.id_detalle} (Factura: {self.id_factura}) - {self.descripcion}>"
    
    @staticmethod
    def create(id_factura, descripcion, cantidad, precio_unitario):
        """Crea un nuevo detalle de factura."""
        conn = database.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO Detalle_Factura (id_factura, descripcion, cantidad, precio_unitario) VALUES (?, ?, ?, ?)",
                (id_factura, descripcion, cantidad, precio_unitario)
            )
            conn.commit()
            return DetalleFactura.get_by_id(cursor.lastrowid)
        except sqlite3.Error as e:
            print(f"Error al crear detalle de factura: {e}")
            return None
        finally:
            conn.close()
    
    @staticmethod
    def get_by_id(id_detalle):
        """Obtiene un detalle de factura por su ID."""
        conn = database.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Detalle_Factura WHERE id_detalle = ?", (id_detalle,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return DetalleFactura(*row)
        return None