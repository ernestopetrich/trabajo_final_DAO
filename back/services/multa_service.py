from models.multa import Multa

class MultaService:

    @staticmethod
    def create(data):
        return Multa.create(**data)

    @staticmethod
    def get_by_id_multa(id_multa):
        return Multa.get_by_id(id_multa)

    @staticmethod
    def get_all():
        return Multa.get_all()
