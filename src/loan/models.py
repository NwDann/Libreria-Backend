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

class LoanHistoryResponse(BaseModel):
    id: int
    usuario_id: int
    ejemplar_id: int
    fecha_prestamo: date
    fecha_prevista: date
    fecha_devolucion: date
    estado: bool
    multa_id: Optional[int]
    
    class Config:
        from_attributes = True

class UserLoansResponse(BaseModel):
    prestamos_activos: List[LoanResponse]
    prestamos_historial: List[LoanHistoryResponse]