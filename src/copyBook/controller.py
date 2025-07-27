from fastapi import APIRouter, Depends, status
from .models import CopyResponse, CopyCreate
from .service import CopyService
from ...database.core import DbSession

router = APIRouter(prefix="/copies", tags=["copies"])

@router.post("/", response_model=CopyResponse, status_code=status.HTTP_201_CREATED)
async def create_copy(copy_data: CopyCreate, db: DbSession = Depends()):
    return CopyService.create_copy(db, copy_data)

@router.get("/{copy_id}/status", response_model=CopyResponse)
async def get_copy_status(copy_id: int, db: DbSession = Depends()):
    return CopyService.get_copy_status(db, copy_id)