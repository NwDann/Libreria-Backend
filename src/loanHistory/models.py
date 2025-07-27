from pydantic import BaseModel
from datetime import date
from typing import Optional

class LoanHistoryResponse(BaseModel):
    id: int
    usuario_id: int
    ejemplar_id: int
    fecha_prestamo: date
    fecha_prevista: date
    fecha_devolucion: date
    estado: bool
    multa_id: Optional[int] = None
    
    class Config:
        from_attributes = True