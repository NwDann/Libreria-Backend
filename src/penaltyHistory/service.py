from sqlalchemy.orm import Session
from typing import List
from ..entities import MultaHist
from .models import PenaltyHistoryResponse
from ...exceptions import PenaltyHistoryNotFoundError

class PenaltyHistoryService:
    @staticmethod
    def get_penalty_history_by_user(db: Session, user_id: int) -> List[PenaltyHistoryResponse]:
        history = db.query(MultaHist).filter(
            MultaHist.usuario_id == user_id
        ).order_by(MultaHist.fecha_inicio.desc()).all()
        
        return [PenaltyHistoryResponse.model_validate(record) for record in history]

    @staticmethod
    def get_all_penalty_history(db: Session) -> List[PenaltyHistoryResponse]:
        history = db.query(MultaHist).order_by(MultaHist.fecha_inicio.desc()).all()
        
        if not history:
            raise PenaltyHistoryNotFoundError()
            
        return [PenaltyHistoryResponse.model_validate(record) for record in history]