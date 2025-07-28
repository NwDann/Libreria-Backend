from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from ..models.loan_mdl import LoanResponse, LoanCreate, LoanReturnResponse
from ..services.loan_svc import LoanService
from ..database.core import DbSession
from ..auth.service import CurrentUser

router = APIRouter(prefix="/loans", tags=["loans"])

@router.post("/", response_model=LoanResponse, status_code=status.HTTP_201_CREATED)
async def create_loan(
    loan_data: LoanCreate, 
    db: DbSession,
    current_user: CurrentUser
):
    if current_user.user_id != loan_data.usuario_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No puedes realizar préstamos para otros usuarios"
        )
    return LoanService.create_loan(db, loan_data)

@router.get("/my-loans", response_model=List[LoanResponse])
async def get_my_loans(
    db: DbSession,
    user_id: int
):
    return LoanService.get_active_loans(db, user_id)

@router.post("/{loan_id}/return", response_model=LoanReturnResponse)
async def return_loan(
    loan_id: int,
    db: DbSession,
    current_user: CurrentUser
):
    try:
        return LoanService.return_loan(db, loan_id, current_user.user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )