from sqlalchemy import (
  Column,
  ForeignKey,
  UniqueConstraint,
  String,
  Integer
)
from sqlalchemy.orm import relationship
from ..database.core import Base

class Recomendacion(Base):
    __tablename__ = "recomendaciones"
    id = Column(Integer, primary_key=True)
    origen_id = Column(Integer, ForeignKey("libros.id"), nullable=False)
    recomendado_id = Column(Integer, ForeignKey("libros.id"), nullable=False)
    comentario = Column(String(500))

    __table_args__ = (
        UniqueConstraint("origen_id", "recomendado_id", name="uq_origen_recomendado"),
    )

    libro_origen = relationship("Libro", foreign_keys=[origen_id], back_populates="recomendaciones_origen")
    libro_recomendado = relationship("Libro", foreign_keys=[recomendado_id], back_populates="recomendaciones_destino")