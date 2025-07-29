from datetime import date, timedelta
from sqlalchemy.orm import Session
from ..entities.loan import Prestamo
from ..entities.loanHistory import PrestamoHist
from ..entities.penalty import Multa
from ..entities.user import Usuario
from ..entities.copyBook import Ejemplar
from ..models.loan_mdl import LoanCreate, LoanResponse, LoanReturnResponse
from typing import List
from ..auth.service import CurrentUser
from ..exceptions import (
    UserNotFoundError, 
    CopyNotFoundError,
    LoanLimitExceededError,
    CopyNotAvailableError,
    UserBlockedError,
    LoanNotFoundError
)

class LoanService:
    @staticmethod
    def create_loan(db: Session, loan_data: LoanCreate, current_user: CurrentUser) -> LoanResponse:
        user_id = current_user.user_id
        if user_id is None:
            raise UserNotFoundError()
        
        user = db.query(Usuario).filter(Usuario.id == user_id).first()
        if not user:
            raise UserNotFoundError(user_id)
            
        if user.estado != "ACTIVO":
            raise UserBlockedError()
            
        max_loans = 5 if user.tipo == "ALUMNO" else 8
        current_loans = db.query(Prestamo).filter(
            Prestamo.usuario_id == user_id
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
            usuario_id=user_id,
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


    @staticmethod
    def return_loan(db: Session, loan_id: int, user_id: int) -> LoanReturnResponse:
        loan = db.query(Prestamo).filter(
            Prestamo.id == loan_id,
            Prestamo.usuario_id == user_id
        ).first()
        
        if not loan:
            raise LoanNotFoundError(loan_id)
        
        # Verificar si hay retraso
        is_late = date.today() > loan.fecha_prevista
        late_days = (date.today() - loan.fecha_prevista).days if is_late else 0
        
        # Mover a histórico
        hist_record = PrestamoHist(
            usuario_id=loan.usuario_id,
            ejemplar_id=loan.ejemplar_id,
            fecha_prestamo=loan.fecha_prestamo,
            fecha_prevista=loan.fecha_prevista,
            fecha_devolucion=date.today(),
            estado=not is_late  # True = Devuelto a tiempo, False = Devuelto con retraso
        )
        
        db.add(hist_record)
        db.delete(loan)
        db.commit()
        
        response = LoanReturnResponse(
            success=True,
            message="Libro devuelto correctamente",
            penalty_applied=is_late,
            penalty_days=late_days
        )
        
        return response