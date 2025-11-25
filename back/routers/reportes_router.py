from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from services.reporte_service import ReportesService

router = APIRouter(prefix="/reporte", tags=["Reportes"])

@router.get("/flota/pdf", response_class=StreamingResponse)
def reporte_flota_pdf():
    pdf_file = ReportesService.reporte_flota()
    return StreamingResponse(
        pdf_file,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=reporte_flota.pdf"}
    )

@router.get("/reportes/pdf/alquileres-por-cliente")
def pdf_alquileres_por_cliente():
    return ReportesService.generar_pdf_alquileres_por_cliente()

@router.get("/reportes/pdf/vehiculos-mas-alquilados")
def pdf_vehiculos_mas():
    return ReportesService.generar_pdf_vehiculos_mas()

@router.get("/reportes/pdf/alquileres-por-mes")
def pdf_alquileres_mes():
    return ReportesService.generar_pdf_alquileres_mes()

@router.get("/reportes/pdf/facturacion-mensual")
def pdf_facturacion():
    return ReportesService.generar_pdf_facturacion()

