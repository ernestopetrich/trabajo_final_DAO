# back/models/state_alquiler.py
from datetime import datetime

class EstadoAlquiler:
    """Interfaz mínima: sólo definimos devolver()."""
    def devolver(self, alquiler):
        raise NotImplementedError("No se puede devolver desde este estado.")


class EstadoActivo(EstadoAlquiler):
    """Solo desde activo se puede devolver: setea estado y fecha real."""
    def devolver(self, alquiler):
        # Delegamos las actualizaciones al modelo (no a la BD directamente aquí)
        # Para evitar import circular, asumimos que alquiler tiene los métodos:
        #   set_fecha_fin_real(fecha) y set_estado(nuevo_estado)
        ahora_iso = datetime.now().isoformat()
        alquiler.set_fecha_fin_real(ahora_iso)
        alquiler.set_estado("finalizado")
        return alquiler


class EstadoFinalizado(EstadoAlquiler):
    """No se puede devolver si ya está finalizado."""
    def devolver(self, alquiler):
        raise Exception("El alquiler ya está finalizado.")
