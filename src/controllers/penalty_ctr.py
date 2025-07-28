from fastapi import APIRouter, Depends
from ..models.penalty_mdl import PenaltyResponse
from ..services.penalty_svc import PenaltyService
from ..database.core import DbSession
from ..auth.service import CurrentUser

router = APIRouter(prefix="/penalties", tags=["penalties"])

@router.get("/my-penalty", response_model=PenaltyResponse)
async def get_my_penalty(
    db: DbSession,
    user_id: int  # Query parameter
):
    PenaltyService.check_and_apply_penalties(db, user_id)
    return PenaltyService.get_active_penalty(db, user_id)
