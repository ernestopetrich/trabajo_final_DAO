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
