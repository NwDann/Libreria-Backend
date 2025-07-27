from sqlalchemy.orm import Session
from typing import List
from ..entities import PrestamoHist
from .models import LoanHistoryResponse
from ...exceptions import LoanHistoryNotFoundError

class LoanHistoryService:
    @staticmethod
    def create_history_record(db: Session, loan_data: dict) -> LoanHistoryResponse:
        record = PrestamoHist(**loan_data)
        db.add(record)
        db.commit()
        return LoanHistoryResponse.model_validate(record)
    
    @staticmethod
    def get_by_user(db: Session, user_id: int) -> List[LoanHistoryResponse]:
        records = db.query(PrestamoHist).filter_by(usuario_id=user_id).all()
        return [LoanHistoryResponse.model_validate(r) for r in records]
    
    @staticmethod
    def get_by_copy(db: Session, copy_id: int) -> List[LoanHistoryResponse]:
        records = db.query(PrestamoHist).filter_by(ejemplar_id=copy_id).all()
        if not records:
            raise LoanHistoryNotFoundError()
        return [LoanHistoryResponse.model_validate(r) for r in records]