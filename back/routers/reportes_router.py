from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from services.reporte_service import ReportesService

router = APIRouter(prefix="/reportes", tags=["Reportes"])

@router.get("/flota/pdf", response_class=StreamingResponse)
def reporte_flota_pdf():
    pdf_file = ReportesService.reporte_flota()
    return StreamingResponse(
        pdf_file,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=reporte_flota.pdf"}
    )

@router.get("/pdf/alquileres-por-cliente")
def descargar_reporte_clientes():
    pdf_buffer = ReportesService.reporte_alquileres_por_cliente()
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=reporte_clientes_alquileres.pdf"}
    )

@router.get("/pdf/vehiculos-mas-alquilados")
def descargar_ranking_vehiculos():
    """Descarga el PDF con el gráfico de torta de vehículos más alquilados."""
    pdf_buffer = ReportesService.reporte_ranking_vehiculos()
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=ranking_vehiculos.pdf"}
    )

@router.get("/pdf/alquileres-por-mes")
def descargar_reporte_mensual():
    """Descarga el reporte de evolución mensual de alquileres."""
    pdf_buffer = ReportesService.reporte_alquileres_mensuales()
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=reporte_mensual.pdf"}
    )

@router.get("/pdf/facturacion-mensual")
def descargar_reporte_facturacion():
    pdf_buffer = ReportesService.reporte_facturacion_mensual()
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=reporte_facturacion_mensual.pdf"}
    )
