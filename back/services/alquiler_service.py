from models.alquiler import Alquiler
from services.vehiculo_service import VehiculoService

class AlquilerService:

    @staticmethod
    def create(data):
        return Alquiler.create(**data)

    @staticmethod
    def get_by_id(id_alquiler):
        return Alquiler.get_by_id(id_alquiler)

    @staticmethod
    def get_all():
        return Alquiler.get_all()

    @staticmethod
    def devolver(id_alquiler):
        alquiler = Alquiler.get_by_id(id_alquiler)
        if not alquiler:
            return None

        # Usar el método real que actualiza fecha_hora_fin_real
        alquiler.devolver()

        # Recargar desde la BD para obtener los datos actualizados
        alquiler_actualizado = Alquiler.get_by_id(id_alquiler)

        return alquiler_actualizado
    
    @staticmethod
    def delete(id_alquiler):
        alquiler = Alquiler.get_by_id(id_alquiler)
        if not alquiler:
            return False
        rtn = alquiler.update_estado("eliminado")
        vehiculo = alquiler.id_vehiculo
        VehiculoService.update(vehiculo, {"estado": "disponible"})
        return rtn
