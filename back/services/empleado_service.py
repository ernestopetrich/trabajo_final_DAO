from models.empleado import Empleado

class EmpleadoService:

    @staticmethod
    def create(data):
        return Empleado.create(**data)

    @staticmethod
    def get_all():
        return Empleado.get_all()

    @staticmethod
    def get_by_id(id_empleado):
        return Empleado.get_by_id(id_empleado)

    @staticmethod
    def get_by_dni(dni):
        return Empleado.get_by_dni(dni)
