from datetime import date, timedelta
from sqlalchemy.orm import Session
from ..entities import Multa, MultaHist, Usuario, Prestamo
from .models import PenaltyResponse
from ...exceptions import UserNotFoundError, NoActivePenaltyError

class PenaltyService:
    @staticmethod
    def check_and_apply_penalties(db: Session, user_id: int) -> None:
        user = db.query(Usuario).filter(Usuario.id == user_id).first()
        if not user:
            raise UserNotFoundError(user_id)
            
        overdue_loans = db.query(Prestamo).filter(
            Prestamo.usuario_id == user_id,
            Prestamo.fecha_prevista < date.today()
        ).all()
        
        if overdue_loans:
            total_days = sum(
                (date.today() - loan.fecha_prevista).days 
                for loan in overdue_loans
            )
            
            penalty = db.query(Multa).filter(
                Multa.usuario_id == user_id,
                Multa.fecha_fin >= date.today()
            ).first()
            
            if penalty:
                penalty.dias_acumulados += total_days
                penalty.fecha_fin = penalty.fecha_inicio + timedelta(days=penalty.dias_acumulados * 2)
            else:
                penalty = Multa(
                    usuario_id=user_id,
                    fecha_inicio=date.today(),
                    dias_acumulados=total_days,
                    fecha_fin=date.today() + timedelta(days=total_days * 2)
                )
                db.add(penalty)
            
            user.estado = "MULTADO"
            db.commit()

    @staticmethod
    def get_active_penalty(db: Session, user_id: int) -> PenaltyResponse:
        penalty = db.query(Multa).filter(
            Multa.usuario_id == user_id,
            Multa.fecha_fin >= date.today()
        ).first()
        
        if not penalty:
            raise NoActivePenaltyError()
            
        return PenaltyResponse.model_validate(penalty)
