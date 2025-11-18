from models.factura import Factura

class FacturaService:

    @staticmethod
    def create(data):
        return Factura.create(**data)

    @staticmethod
    def get_by_alquiler(id_alquiler):
        return Factura.get_by_alquiler(id_alquiler)

    @staticmethod
    def get_by_id(id_factura):
        return Factura.get_by_id(id_factura)

    @staticmethod
    def get_all():
        return Factura.get_all()

    @staticmethod
    def update(id_factura, data):
        return Factura.update(id_factura, data)