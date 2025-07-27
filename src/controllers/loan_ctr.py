from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from ..models.loan_mdl import LoanResponse, LoanCreate
from ..services.loan_svc import LoanService
from ..database.core import DbSession
from ..auth.service import CurrentUser

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

@router.get("/my-loans", response_model=List[LoanResponse])
async def get_my_loans(
    db: DbSession = Depends(),
    current_user: CurrentUser = Depends()
):
    return LoanService.get_active_loans(db, current_user.user_id)