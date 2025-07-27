from datetime import date, timedelta
from sqlalchemy.orm import Session
from ..entities import Prestamo, Usuario, Ejemplar
from .models import LoanResponse
from ...exceptions import (
    UserNotFoundError, 
    CopyNotFoundError,
    LoanLimitExceededError,
    CopyNotAvailableError,
    UserBlockedError
)

class LoanService:
    @staticmethod
    def create_loan(db: Session, loan_data: LoanCreate) -> LoanResponse:
        user = db.query(Usuario).filter(Usuario.id == loan_data.usuario_id).first()
        if not user:
            raise UserNotFoundError(loan_data.usuario_id)
            
        if user.estado != "ACTIVO":
            raise UserBlockedError()
            
        max_loans = 5 if user.tipo == "alumno" else 8
        current_loans = db.query(Prestamo).filter(
            Prestamo.usuario_id == loan_data.usuario_id
        ).count()
        
        if current_loans >= max_loans:
            raise LoanLimitExceededError()
            
        copy = db.query(Ejemplar).filter(Ejemplar.id == loan_data.ejemplar_id).first()
        if not copy:
            raise CopyNotFoundError(loan_data.ejemplar_id)
            
        if copy.prestamos:
            raise CopyNotAvailableError()
            
        loan_days = 7 if user.tipo == "alumno" else 30
        new_loan = Prestamo(
            usuario_id=loan_data.usuario_id,
            ejemplar_id=loan_data.ejemplar_id,
            fecha_prestamo=date.today(),
            fecha_prevista=date.today() + timedelta(days=loan_days)
        )
        
        db.add(new_loan)
        db.commit()
        return LoanResponse.model_validate(new_loan)

    @staticmethod
    def get_active_loans(db: Session, user_id: int) -> List[LoanResponse]:
        loans = db.query(Prestamo).filter(Prestamo.usuario_id == user_id).all()
        return [LoanResponse.model_validate(loan) for loan in loans]