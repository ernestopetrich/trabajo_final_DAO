from models.detalle_factura import DetalleFactura

class DetalleFacturaService:

    @staticmethod
    def create(data):
        return DetalleFactura.create(**data)

    @staticmethod
    def get_by_id_factura(id_factura):
        return DetalleFactura.get_by_id_factura(id_factura)

    @staticmethod
    def get_by_id(id_detalle):
        return DetalleFactura.get_by_id(id_detalle)

    @staticmethod
    def get_all():
        return DetalleFactura.get_all()