from fastapi import APIRouter, Depends
from typing import List
from .models import PenaltyHistoryResponse
from .service import PenaltyHistoryService
from ...database.core import DbSession
from ...auth.service import CurrentUser

router = APIRouter(prefix="/penalties-history", tags=["penalties-history"])

@router.get("/my-history", response_model=List[PenaltyHistoryResponse])
async def get_my_penalty_history(
    db: DbSession = Depends(),
    current_user: CurrentUser = Depends()
):
    return PenaltyHistoryService.get_by_user(db, current_user.user_id)

@router.get("/", response_model=List[PenaltyHistoryResponse])
async def get_all_penalty_history(db: DbSession = Depends()):
    return PenaltyHistoryService.get_all(db)