from pydantic import BaseModel
from datetime import date

class LoanCreate(BaseModel):
    ejemplar_id: int

class LoanResponse(BaseModel):
    id: int
    usuario_id: int
    ejemplar_id: int
    fecha_prestamo: date
    fecha_prevista: date
    
    class Config:
        from_attributes = True

class LoanReturnResponse(BaseModel):
    success: bool
    message: str
    penalty_applied: bool = False
    penalty_days: int = 0

    class Config:
        from_attributes = True
