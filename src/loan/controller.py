from fastapi import APIRouter, Depends, status, HTTPException
from .models import LoanResponse, LoanCreate, UserLoansResponse, LoanHistoryResponse
from .service import LoanService
from ...database.core import DbSession
from ...auth.service import CurrentUser

router = APIRouter(prefix="/loans", tags=["loans"])

@router.post("/", response_model=LoanResponse, status_code=status.HTTP_201_CREATED)
async def create_loan(
    loan_data: LoanCreate, 
    db: DbSession = Depends(),
    current_user: CurrentUser = Depends()
):
    if current_user.user_id != loan_data.usuario_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No puedes realizar préstamos para otros usuarios"
        )
    return LoanService.create_loan(db, loan_data)

@router.post("/{loan_id}/return", response_model=LoanHistoryResponse)
async def return_loan(
    loan_id: int,
    db: DbSession = Depends(),
    current_user: CurrentUser = Depends()
):
    return LoanService.return_loan(db, loan_id, current_user.user_id)

@router.get("/my-loans", response_model=UserLoansResponse)
async def get_my_loans(
    db: DbSession = Depends(),
    current_user: CurrentUser = Depends()
):
    return LoanService.get_user_loans(db, current_user.user_id)