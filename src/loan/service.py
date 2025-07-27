from datetime import date, timedelta
from sqlalchemy.orm import Session
from ..entities import Prestamo, PrestamoHist, Usuario, Ejemplar, Multa
from .models import LoanResponse, LoanHistoryResponse, UserLoansResponse
from ...exceptions import (
    UserNotFoundError, 
    CopyNotFoundError,
    LoanLimitExceededError,
    CopyNotAvailableError,
    UserBlockedError,
    LoanNotFoundError
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
        db.refresh(new_loan)
        return LoanResponse.model_validate(new_loan)

    @staticmethod
    def return_loan(db: Session, loan_id: int, user_id: int) -> LoanHistoryResponse:
        loan = db.query(Prestamo).filter(
            Prestamo.id == loan_id,
            Prestamo.usuario_id == user_id
        ).first()
        
        if not loan:
            raise LoanNotFoundError()
            
        # Crear registro histórico
        loan_hist = PrestamoHist(
            usuario_id=loan.usuario_id,
            ejemplar_id=loan.ejemplar_id,
            fecha_prestamo=loan.fecha_prestamo,
            fecha_prevista=loan.fecha_prevista,
            fecha_devolucion=date.today(),
            estado=True
        )
        
        # Verificar si hubo retraso
        days_late = (date.today() - loan.fecha_prevista).days
        if days_late > 0:
            penalty = db.query(Multa).filter(
                Multa.usuario_id == user_id,
                Multa.fecha_fin >= date.today()
            ).first()
            
            if penalty:
                penalty.dias_acumulados += days_late
                penalty.fecha_fin = penalty.fecha_inicio + timedelta(days=penalty.dias_acumulados * 2)
            else:
                penalty = Multa(
                    usuario_id=user_id,
                    fecha_inicio=date.today(),
                    dias_acumulados=days_late,
                    fecha_fin=date.today() + timedelta(days=days_late * 2)
                )
                db.add(penalty)
            
            loan_hist.multa_id = penalty.id
        
        db.add(loan_hist)
        db.delete(loan)
        db.commit()
        return LoanHistoryResponse.model_validate(loan_hist)

    @staticmethod
    def get_user_loans(db: Session, user_id: int) -> UserLoansResponse:
        active_loans = db.query(Prestamo).filter(
            Prestamo.usuario_id == user_id
        ).all()
        
        history_loans = db.query(PrestamoHist).filter(
            PrestamoHist.usuario_id == user_id
        ).all()
        
        return UserLoansResponse(
            prestamos_activos=[LoanResponse.model_validate(loan) for loan in active_loans],
            prestamos_historial=[LoanHistoryResponse.model_validate(loan) for loan in history_loans]
        )