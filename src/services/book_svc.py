from sqlalchemy.orm import Session
from ..entities.book import Libro
from ..models.book_mdl import BookResponse, BookWithCopies, BookWithRecommendations
from ..exceptions import BookNotFoundError
from typing import List

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
    def get_book_details(db: Session, book_id: int) -> BookWithCopies:
        book = db.query(Libro).filter(Libro.id == book_id).first()
        if not book:
            raise BookNotFoundError(book_id)
        
        return BookWithCopies(
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
    def get_book_recommendations(db: Session, book_id: int) -> BookWithRecommendations:
        book = db.query(Libro).filter(Libro.id == book_id).first()
        if not book:
            raise BookNotFoundError(book_id)
            
        return BookWithRecommendations(
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