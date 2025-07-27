from sqlalchemy.orm import Session
from datetime import date
from ..entities import Ejemplar, Libro
from .models import CopyResponse
from ...exceptions import BookNotFoundError, CopyNotFoundError

class CopyService:
    @staticmethod
    def create_copy(db: Session, copy_data: CopyCreate) -> CopyResponse:
        if not db.query(Libro).filter(Libro.id == copy_data.libro_id).first():
            raise BookNotFoundError(copy_data.libro_id)
            
        new_copy = Ejemplar(
            codigo=copy_data.codigo,
            libro_id=copy_data.libro_id,
            fecha_adquisicion=date.today(),
            observaciones=copy_data.observaciones
        )
        
        db.add(new_copy)
        db.commit()
        db.refresh(new_copy)
        return CopyResponse(
            id=new_copy.id,
            codigo=new_copy.codigo,
            libro_id=new_copy.libro_id,
            fecha_adquisicion=new_copy.fecha_adquisicion,
            observaciones=new_copy.observaciones,
            disponible=True
        )

    @staticmethod
    def get_copy_status(db: Session, copy_id: int) -> CopyResponse:
        copy = db.query(Ejemplar).filter(Ejemplar.id == copy_id).first()
        if not copy:
            raise CopyNotFoundError(copy_id)
            
        return CopyResponse(
            id=copy.id,
            codigo=copy.codigo,
            libro_id=copy.libro_id,
            fecha_adquisicion=copy.fecha_adquisicion,
            observaciones=copy.observaciones,
            disponible=not bool(copy.prestamos)
        )