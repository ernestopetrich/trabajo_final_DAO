import database
import sqlite3 # Importar sqlite3 para manejar IntegrityError

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
        self.fecha_hora_inicio = fecha_hora_inicio
        self.fecha_hora_fin_prevista = fecha_hora_fin_prevista
        self.fecha_hora_fin_real = fecha_hora_fin_real
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

# Puedes seguir añadiendo las clases para Empleado, Mantenimiento, Multa, Danio, etc.
# siguiendo el mismo patrón.