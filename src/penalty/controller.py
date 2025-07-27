from fastapi import APIRouter, Depends
from typing import List
from .models import PenaltyResponse, PenaltyHistoryResponse
from .service import PenaltyService
from ...database.core import DbSession
from ...auth.service import CurrentUser

router = APIRouter(prefix="/penalties", tags=["penalties"])

@router.get("/my-penalty", response_model=PenaltyResponse)
async def get_my_penalty(
    db: DbSession = Depends(),
    current_user: CurrentUser = Depends()
):
    PenaltyService.check_and_apply_penalties(db, current_user.user_id)
    return PenaltyService.get_active_penalty(db, current_user.user_id)

@router.get("/my-history", response_model=List[PenaltyHistoryResponse])
async def get_my_penalty_history(
    db: DbSession = Depends(),
    current_user: CurrentUser = Depends()
):
    return PenaltyService.get_penalty_history(db, current_user.user_id)