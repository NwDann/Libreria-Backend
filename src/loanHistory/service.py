from sqlalchemy.orm import Session
from typing import List
from ..entities import PrestamoHist
from .models import LoanHistoryResponse
from ...exceptions import LoanHistoryNotFoundError

class LoanHistoryService:
    @staticmethod
    def get_loan_history_by_user(db: Session, user_id: int) -> List[LoanHistoryResponse]:
        history = db.query(PrestamoHist).filter(
            PrestamoHist.usuario_id == user_id
        ).order_by(PrestamoHist.fecha_prestamo.desc()).all()
        
        return [LoanHistoryResponse.model_validate(record) for record in history]

    @staticmethod
    def get_loan_history_by_copy(db: Session, copy_id: int) -> List[LoanHistoryResponse]:
        history = db.query(PrestamoHist).filter(
            PrestamoHist.ejemplar_id == copy_id
        ).order_by(PrestamoHist.fecha_prestamo.desc()).all()
        
        if not history:
            raise LoanHistoryNotFoundError()
            
        return [LoanHistoryResponse.model_validate(record) for record in history]