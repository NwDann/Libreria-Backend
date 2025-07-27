from pydantic import BaseModel
from datetime import date

class PenaltyResponse(BaseModel):
    id: int
    usuario_id: int
    fecha_inicio: date
    dias_acumulados: int
    fecha_fin: date
    
    class Config:
        from_attributes = True
