from models.alquiler import Alquiler

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
        if alquiler:
            alquiler.devolver()
            return alquiler
        return None
