from models.mantenimiento import Mantenimiento

class MantenimientoService:

    @staticmethod
    def create(data):
        return Mantenimiento.create(**data)

    @staticmethod
    def get_by_id(id_mantenimiento):
        return Mantenimiento.get_by_id(id_mantenimiento)

    @staticmethod
    def get_all():
        return Mantenimiento.get_all()
