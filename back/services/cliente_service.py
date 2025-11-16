from models.cliente import Cliente

class ClienteService:

    @staticmethod
    def create(data):
        return Cliente.create(**data)

    @staticmethod
    def get_by_id(id_cliente):
        return Cliente.get_by_id(id_cliente)

    @staticmethod
    def get_by_dni(dni):
        return Cliente.get_by_dni(dni)

    @staticmethod
    def get_all():
        print("Error 2")
        return Cliente.get_all()

    @staticmethod
    def update(id_cliente, data):
        return Cliente.update(id_cliente, **data)

    @staticmethod
    def delete(id_cliente):
        return Cliente.delete(id_cliente)
