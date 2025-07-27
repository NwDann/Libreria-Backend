from sqlalchemy.orm import Session
from typing import List
from ..entities.penaltyHistory import MultaHist
from ..models.penaltyHistory_mdl import PenaltyHistoryResponse
from ..exceptions import PenaltyHistoryNotFoundError

class PenaltyHistoryService:
    @staticmethod
    def get_by_user(db: Session, user_id: int) -> List[PenaltyHistoryResponse]:
        records = db.query(MultaHist).filter_by(usuario_id=user_id).all()
        return [PenaltyHistoryResponse.model_validate(r) for r in records]
    
    @staticmethod
    def get_all(db: Session) -> List[PenaltyHistoryResponse]:
        records = db.query(MultaHist).all()
        if not records:
            raise PenaltyHistoryNotFoundError()
        return [PenaltyHistoryResponse.model_validate(r) for r in records]