from models.vehiculo import Vehiculo

class VehiculoService:

    @staticmethod
    def create(data):
        return Vehiculo.create(**data)

    @staticmethod
    def get_all():
        return Vehiculo.get_all()

    @staticmethod
    def get_by_id(id_vehiculo):
        return Vehiculo.get_by_id(id_vehiculo)

    @staticmethod
    def update(id_vehiculo, data):
        return Vehiculo.update(id_vehiculo, **data)

    @staticmethod
    def delete(id_vehiculo):
        return Vehiculo.delete(id_vehiculo)

    @staticmethod
    def is_available(id_vehiculo, fecha_inicio, fecha_fin):
        veh = Vehiculo.get_by_id(id_vehiculo)
        if veh:
            return veh.is_available(fecha_inicio, fecha_fin)
        return False
