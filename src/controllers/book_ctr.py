from fastapi import APIRouter, Depends
from typing import List
from ..models.book_mdl import BookResponse, BookWithCopies, BookWithRecommendations
from ..services.book_svc import BookService
from ..database.core import DbSession

router = APIRouter(prefix="/books", tags=["books"])

@router.get("/", response_model=List[BookResponse])
async def get_all_books(db: DbSession):
    return BookService.get_all_books(db)

@router.get("/{book_id}", response_model=BookWithCopies)
async def get_book_details(book_id: int, db: DbSession):
    return BookService.get_book_details(db, book_id)

@router.get("/{book_id}/recommendations", response_model=BookWithRecommendations)
async def get_book_recommendations(book_id: int, db: DbSession):
    return BookService.get_book_recommendations(db, book_id)