from reportlab.pdfgen import canvas
from io import BytesIO
from models.vehiculo import Vehiculo

class ReportesService:

    @staticmethod
    def reporte_flota():
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer)

        pdf.drawString(50, 800, "Reporte - Estado de Flota")
        pdf.drawString(50, 785, "Patente | Marca | Modelo | Precio Diario | Estado")

        y = 765
        vehiculos =Vehiculo.get_all()
        for v in vehiculos:
            linea = f"{v.patente} | {v.marca} | {v.modelo} | ${v.precio_diario} | {v.estado}"
            pdf.drawString(40, y, linea)
            y -= 20
            if y < 40:
                pdf.showPage()
                pdf.setFont("Helvetica", 10)
                y = 800

        pdf.save()
        buffer.seek(0)
        return buffer
