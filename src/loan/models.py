from pydantic import BaseModel
from datetime import date
from typing import List

class LoanCreate(BaseModel):
    usuario_id: int
    ejemplar_id: int

class LoanResponse(BaseModel):
    id: int
    usuario_id: int
    ejemplar_id: int
    fecha_prestamo: date
    fecha_prevista: date
    
    class Config:
        from_attributes = True

