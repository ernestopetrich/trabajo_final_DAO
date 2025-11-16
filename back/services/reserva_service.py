from models.reserva import Reserva

class ReservaService:

    @staticmethod
    def create(data):
        return Reserva.create(**data)

    @staticmethod
    def get_by_id(id_reserva):
        return Reserva.get_by_id(id_reserva)

    @staticmethod
    def get_all():
        return Reserva.get_all()

    @staticmethod
    def update_estado(id_reserva, estado):
        reserva = Reserva.get_by_id(id_reserva)
        if reserva:
            reserva.update_estado(estado)
            return reserva
        return None
