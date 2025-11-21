from datetime import datetime

class EstadoAlquiler:
    """
    Interfaz Base: Define todas las transiciones posibles.
    Por defecto, todas lanzan error. Las subclases habilitan las permitidas.
    """
    def confirmar(self, alquiler):
        raise ValueError(f"No se puede confirmar un alquiler en estado {self.nombre}")

    def iniciar(self, alquiler):
        raise ValueError(f"No se puede iniciar un alquiler en estado {self.nombre}")

    def devolver(self, alquiler):
        raise ValueError(f"No se puede devolver un alquiler en estado {self.nombre}")

    def cancelar(self, alquiler):
        raise ValueError(f"No se puede cancelar un alquiler en estado {self.nombre}")
    
    @property
    def nombre(self):
        return self.__class__.__name__


class EstadoPendiente(EstadoAlquiler):
    def confirmar(self, alquiler):
        alquiler.set_estado("confirmado")
        return "Alquiler confirmado exitosamente."
    
    def cancelar(self, alquiler):
        alquiler.set_estado("cancelado")
        return "Alquiler cancelado."

class EstadoConfirmado(EstadoAlquiler):
    def iniciar(self, alquiler):
        alquiler.set_estado("activo")
        return "Alquiler iniciado. El vehículo está en uso."
    
    def cancelar(self, alquiler):
        alquiler.set_estado("cancelado")
        return "Reserva confirmada ha sido cancelada."

class EstadoActivo(EstadoAlquiler):
    def devolver(self, alquiler):
        # 1. Establecer la fecha de fin real (AHORA)
        ahora_iso = datetime.now().isoformat()
        alquiler.set_fecha_fin_real(ahora_iso)
        
        # --- AQUÍ ES DONDE SE LLAMA A LA LÓGICA DE COSTOS ---
        # 2. Calcular el costo total (Días + Multas + Daños)
        # Esto usa la fecha real que acabamos de poner vs la fecha de inicio
        costo = alquiler.calcular_y_guardar_costo()
        
        # 3. Cambiar estado a finalizado
        alquiler.set_estado("finalizado")
        
        # 4. Liberar vehículo en la BD
        # Importamos database aquí dentro para evitar problemas de importación circular
        import database 
        conn = database.get_db_connection()
        # Liberamos el vehículo (estado 'disponible')
        conn.execute("UPDATE Vehiculos SET estado = 'disponible' WHERE id_vehiculo = ?", (alquiler.id_vehiculo,))
        conn.commit()
        conn.close()

        return f"Vehículo devuelto. Alquiler finalizado. Costo total calculado: ${costo}"

class EstadoFinalizado(EstadoAlquiler):
    pass 

class EstadoCancelado(EstadoAlquiler):
    pass