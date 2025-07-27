from sqlalchemy.orm import Session
from ..entities import Libro
from .models import BookResponse, BookWithCopiesResponse, BookWithRecommendationsResponse
from ...exceptions import BookNotFoundError

class BookService:
    @staticmethod
    def get_all_books(db: Session) -> List[BookResponse]:
        books = db.query(Libro).all()
        return [BookResponse(
            id=book.id,
            isbn=book.isbn,
            titulo=book.titulo,
            autor=book.autor,
            num_paginas=book.num_paginas,
            total_ejemplares=book.total_ejemplares,
            portada_uri=book.portada_uri,
            ejemplares_disponibles=sum(1 for copy in book.ejemplares if not copy.prestamos)
        ) for book in books]

    @staticmethod
    def get_book_details(db: Session, book_id: int) -> BookWithCopiesResponse:
        book = db.query(Libro).filter(Libro.id == book_id).first()
        if not book:
            raise BookNotFoundError(book_id)
        
        return BookWithCopiesResponse(
            id=book.id,
            isbn=book.isbn,
            titulo=book.titulo,
            autor=book.autor,
            num_paginas=book.num_paginas,
            total_ejemplares=book.total_ejemplares,
            portada_uri=book.portada_uri,
            ejemplares_disponibles=sum(1 for copy in book.ejemplares if not copy.prestamos),
            ejemplares=book.ejemplares
        )

    @staticmethod
    def get_book_recommendations(db: Session, book_id: int) -> BookWithRecommendationsResponse:
        book = db.query(Libro).filter(Libro.id == book_id).first()
        if not book:
            raise BookNotFoundError(book_id)
            
        return BookWithRecommendationsResponse(
            id=book.id,
            isbn=book.isbn,
            titulo=book.titulo,
            autor=book.autor,
            num_paginas=book.num_paginas,
            total_ejemplares=book.total_ejemplares,
            portada_uri=book.portada_uri,
            ejemplares_disponibles=sum(1 for copy in book.ejemplares if not copy.prestamos),
            recomendaciones=book.recomendaciones_destino
        )