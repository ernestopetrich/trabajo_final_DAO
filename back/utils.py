from datetime import datetime

def to_iso(dt_str):
    """Convierte cualquier formato usable a 'YYYY-MM-DD HH:MM:SS'."""
    formatos = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%Y"
    ]
    for f in formatos:
        try:
            dt = datetime.strptime(dt_str, f)
            # si no tiene hora, agregar 00:00:00
            if f in ["%Y-%m-%d", "%d/%m/%Y"]:
                return dt.strftime("%Y-%m-%d 00:00:00")
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except:
            pass
    raise ValueError(f"Formato de fecha inválido: {dt_str}")
