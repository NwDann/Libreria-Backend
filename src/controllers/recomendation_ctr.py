from fastapi import APIRouter, Depends, status
from typing import List
from ..models.recomendation_mdl import RecommendationResponse, RecommendationCreate
from ..services.recomendation_svc import RecommendationService
from ..database.core import DbSession

router = APIRouter(prefix="/recommendations", tags=["recommendations"])

@router.post("/", response_model=RecommendationResponse, status_code=status.HTTP_201_CREATED)
async def create_recommendation(
    data: RecommendationCreate, 
    db: DbSession
):
    return RecommendationService.create_recommendation(db, data)

@router.get("/book/{book_id}", response_model=List[RecommendationResponse])
async def get_book_recommendations(
    book_id: int, 
    db: DbSession
):
    return RecommendationService.get_recommendations_for_book(db, book_id)