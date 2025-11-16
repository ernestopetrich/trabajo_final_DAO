# Permite que FastAPI importe los routers fácilmente
from .cliente_router import router as cliente_router
from .empleado_router import router as empleado_router
from .vehiculo_router import router as vehiculo_router
from .reserva_router import router as reserva_router
from .alquiler_router import router as alquiler_router
from .mantenimiento_router import router as mantenimiento_router
from .multa_router import router as multa_router
from .danio_router import router as danio_router
from .factura_router import router as factura_router
