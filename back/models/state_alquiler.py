from datetime import datetime
from services.vehiculo_service import VehiculoService
from services.multa_service import MultaService
from services.danio_service import DanioService
from services.vehiculo_service import VehiculoService


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
    
    def eliminar(self, alquiler):
        alquiler.set_estado("eliminado")
        return "Alquiler dado de baja."

class EstadoConfirmado(EstadoAlquiler):
    def iniciar(self, alquiler):
        if datetime.fromisoformat(alquiler.fecha_hora_inicio) >= datetime.now():
            raise ValueError("No se puede iniciar el alquiler antes de la fecha y hora de inicio programada.")
        alquiler.set_estado("activo")
        VehiculoService.update(alquiler.id_vehiculo, {"estado": "alquilado"})
        return "Alquiler iniciado. El vehículo está en uso."
    
    def eliminar(self, alquiler):
        alquiler.set_estado("eliminado")
        return "Reserva confirmada ha sido dada de baja."

class EstadoActivo(EstadoAlquiler):
    def eliminar(self, alquiler):
        raise ValueError("No se puede eliminar un alquiler activo. Debe ser finalizado primero.")
    def devolver(self, alquiler):
        # 1. Establecer la fecha de fin real (AHORA)
        ahora_iso = datetime.now().isoformat()
        alquiler.set_fecha_fin_real(ahora_iso)
        
        # --- AQUÍ ES DONDE SE LLAMA A LA LÓGICA DE COSTOS ---
        # 2. Calcular el costo total (Días + Multas + Daños)
        # Esto usa la fecha real que acabamos de poner vs la fecha de inicio
        costo = alquiler.calcular_y_guardar_costo()
        cantidad_dias = alquiler.calcular_dias_alquiler()
        
        from services.factura_service import FacturaService
        from services.detalle_factura_service import DetalleFacturaService

        factura = FacturaService.create({   "id_alquiler": alquiler.id_alquiler,
                                            "fecha_hora_emision": ahora_iso,
                                            "monto_total": costo,
                                            "estado_pago": "abonado"
                                        })

        vehiculo = VehiculoService.get_by_id(alquiler.id_vehiculo)
        precio_diario = vehiculo.precio_diario

        detalle = DetalleFacturaService.create({
            "id_factura": factura.id_factura,
            "descripcion": f"Alquiler vehículo {vehiculo.marca} {vehiculo.nombre} {vehiculo.modelo} ({vehiculo.patente})",
            "cantidad": cantidad_dias,
            "monto": precio_diario
        })

        multas = MultaService.get_by_id_alquiler(alquiler.id_alquiler)

        if multas:
            for multa in multas:
                detalle_multa = DetalleFacturaService.create({
                    "id_factura": factura.id_factura,
                    "descripcion": f"Multa: {multa.descripcion}",
                    "cantidad": 1,
                    "monto": multa.monto
                })
        
        danios = DanioService.get_by_id_alquiler(alquiler.id_alquiler)
        if danios:
            for danio in danios:
                detalle_danio = DetalleFacturaService.create({
                    "id_factura": factura.id_factura,
                    "descripcion": f"Daño: {danio.descripcion}",
                    "cantidad": 1,
                    "monto": danio.costo_reparacion
                })

        


        # 3. Cambiar estado a finalizado
        alquiler.set_estado("finalizado")
        
        VehiculoService.update(alquiler.id_vehiculo, { "estado": "disponible" })

        return f"Vehículo devuelto. Alquiler finalizado. Costo total calculado: ${costo}"

class EstadoFinalizado(EstadoAlquiler):
    pass 

class EstadoCancelado(EstadoAlquiler):
    pass