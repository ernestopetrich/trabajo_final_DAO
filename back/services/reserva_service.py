
from fastapi import HTTPException
from models.reserva import Reserva
from models.reserva import Reserva as ReservaModel
from models.vehiculo import Vehiculo as VehiculoModel
from models.empleado import Empleado as EmpleadoModel
from models.alquiler import Alquiler as AlquilerModel
from datetime import datetime, timedelta


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
    
    @staticmethod
    def reservaToAlquiler(id_reserva, id_empleado):
        reserva = ReservaModel.get_by_id(id_reserva)
        if not reserva:
            raise HTTPException(status_code=404, detail="Reserva no encontrada")
        
        print(reserva.fecha_inicio, datetime.now().strftime("%Y-%m-%d"))
        print(reserva.fecha_inicio > (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"))

        if reserva.fecha_inicio < datetime.now().strftime("%Y-%m-%d"):
            raise HTTPException(status_code=400, detail="La fecha de inicio de la reserva ya pasó")
        
        elif reserva.fecha_inicio > (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"):
            raise HTTPException(status_code=400, detail="Solo se pueden convertir reservas con hasta 2 días de anticipación")

        if reserva.estado != 'confirmada':
            raise HTTPException(status_code=400, detail="Solo se pueden convertir reservas confirmadas")

        vehiculo = VehiculoModel.get_by_id(reserva.id_vehiculo)
        if not vehiculo:
            raise HTTPException(status_code=404, detail="Vehículo no encontrado")

        empleado = EmpleadoModel.get_by_id(id_empleado)
        if not empleado:
            raise HTTPException(status_code=404, detail="Empleado no encontrado")

        """# Verificar disponibilidad
        if not vehiculo.is_available(reserva.fecha_inicio, reserva.fecha_fin):
            raise HTTPException(status_code=400, detail="Vehículo no disponible en este momento")"""

        # Crear el alquiler
        nuevo_alquiler = AlquilerModel.create(
            id_cliente=reserva.id_cliente,
            id_vehiculo=reserva.id_vehiculo,
            id_empleado=id_empleado,
            fecha_hora_inicio=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            fecha_hora_fin_prevista=reserva.fecha_fin
        )
        
        if not nuevo_alquiler:
            raise HTTPException(status_code=500, detail="Error al crear el alquiler desde la reserva")

        #Borrar la reserva o marcar como convertida
        reserva.delete()

        # Actualizar estado de la reserva
        #reserva.update_estado('convertida')

        return nuevo_alquiler