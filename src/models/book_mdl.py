from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from .copyBook_mdl import CopyResponse
from .recomendation_mdl import RecommendationResponse

class BookBase(BaseModel):
    isbn: str
    titulo: str
    autor: str
    num_paginas: Optional[int] = None
    total_ejemplares: int = 0
    portada_uri: Optional[str] = None  

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: int
    ejemplares_disponibles: int
    
    class Config:
        from_attributes = True

class BookWithCopies(BookResponse):
    ejemplares: List['CopyResponse'] = []

class BookWithRecommendations(BookResponse):
    recomendaciones: List['RecommendationResponse'] = []