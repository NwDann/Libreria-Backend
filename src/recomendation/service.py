from sqlalchemy.orm import Session
from ..entities import Recomendacion, Libro
from .models import RecommendationResponse
from ...exceptions import BookNotFoundError, RecommendationExistsError

class RecommendationService:
    @staticmethod
    def create_recommendation(
        db: Session, 
        data: RecommendationCreate
    ) -> RecommendationResponse:
        if not db.query(Libro).filter(Libro.id == data.origen_id).first():
            raise BookNotFoundError(data.origen_id)
            
        if not db.query(Libro).filter(Libro.id == data.recomendado_id).first():
            raise BookNotFoundError(data.recomendado_id)
            
        if db.query(Recomendacion).filter_by(
            origen_id=data.origen_id,
            recomendado_id=data.recomendado_id
        ).first():
            raise RecommendationExistsError()
            
        new_rec = Recomendacion(
            origen_id=data.origen_id,
            recomendado_id=data.recomendado_id,
            comentario=data.comentario
        )
        
        db.add(new_rec)
        db.commit()
        return RecommendationResponse.model_validate(new_rec)

    @staticmethod
    def get_recommendations_for_book(
        db: Session, 
        book_id: int
    ) -> List[RecommendationResponse]:
        recommendations = db.query(Recomendacion).filter(
            Recomendacion.origen_id == book_id
        ).all()
        
        return [RecommendationResponse.model_validate(rec) for rec in recommendations]