from models.factura import Factura
from schemas.factura_schema import FacturaResponseAlquiler
from services.alquiler_service import AlquilerService
from services.cliente_service import ClienteService
from services.detalle_factura_service import DetalleFacturaService

class FacturaService:

    @staticmethod
    def create(data):
        return Factura.create(**data)

    @staticmethod
    def get_by_alquiler(id_alquiler):
        factura = Factura.get_by_alquiler(id_alquiler)
        print(factura.id_factura)
        alquiler = AlquilerService.get_by_id(id_alquiler)
        cliente = ClienteService.get_by_id(alquiler.id_cliente)
        detallesFactura = DetalleFacturaService.get_by_id_factura(factura.id_factura)

        print(detallesFactura)

        return FacturaResponseAlquiler(
            id_factura=factura.id_factura,
            id_alquiler=alquiler.id_alquiler,
            fecha_hora_emision=factura.fecha_hora_emision,
            monto_total=factura.monto_total,
            cliente=cliente,
            items=detallesFactura,
            subtotal=factura.monto_total,
            impuestos=factura.monto_total * 0.21,
            total=factura.monto_total * 1.21
        )

    @staticmethod
    def get_by_id(id_factura):
        return Factura.get_by_id(id_factura)

    @staticmethod
    def get_all():
        return Factura.get_all()

    @staticmethod
    def update(id_factura, data):
        return Factura.update(id_factura, data)