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
        # Transición: Pendiente -> Confirmado
        alquiler.set_estado("confirmado")
        return "Alquiler confirmado exitosamente."
    
    def cancelar(self, alquiler):
        # Transición: Pendiente -> Cancelado/Eliminado
        alquiler.set_estado("cancelado")
        return "Alquiler cancelado."

class EstadoConfirmado(EstadoAlquiler):
    def iniciar(self, alquiler):
        # Transición: Confirmado -> Activo (El cliente se lleva el auto)
        alquiler.set_estado("activo")
        return "Alquiler iniciado. El vehículo está en uso."
    
    def cancelar(self, alquiler):
        # Transición: Confirmado -> Cancelado
        alquiler.set_estado("cancelado")
        return "Reserva confirmada ha sido cancelada."

class EstadoActivo(EstadoAlquiler):
    def devolver(self, alquiler):
        # Transición: Activo -> Finalizado (El cliente devuelve el auto)
        ahora_iso = datetime.now().isoformat()
        alquiler.set_fecha_fin_real(ahora_iso)
        
        # Aquí también podrías liberar el vehículo en la BD si quisieras
        # alquiler.liberar_vehiculo() 
        
        alquiler.set_estado("finalizado")
        return "Vehículo devuelto. Alquiler finalizado."

class EstadoFinalizado(EstadoAlquiler):
    pass  # No permite ninguna acción, es un estado terminal.

class EstadoCancelado(EstadoAlquiler):
    pass  # No permite ninguna acción, es un estado terminal.