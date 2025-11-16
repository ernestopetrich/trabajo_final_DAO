from models.danio import Danio

class DanioService:

    @staticmethod
    def create(data):
        return Danio.create(**data)

    @staticmethod
    def get_by_id_alquiler(id_alquiler):
        return Danio.get_by_id_alquiler(id_alquiler)

    @staticmethod
    def get_all():
        return Danio.get_all()
