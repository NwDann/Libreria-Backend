from fastapi import APIRouter, Depends
from typing import List
from ..models.loanHistory_mdl import LoanHistoryResponse
from ..services.loanHistory_svc import LoanHistoryService
from ..database.core import DbSession
from ..auth.service import CurrentUser

router = APIRouter(prefix="/loans-history", tags=["loans-history"])

@router.get("/my-history", response_model=List[LoanHistoryResponse])
async def get_my_loan_history(
    db: DbSession = Depends(),
    current_user: CurrentUser = Depends()
):
    return LoanHistoryService.get_by_user(db, current_user.user_id)

@router.get("/copy/{copy_id}", response_model=List[LoanHistoryResponse])
async def get_copy_loan_history(
    copy_id: int,
    db: DbSession = Depends()
):
    return LoanHistoryService.get_by_copy(db, copy_id)