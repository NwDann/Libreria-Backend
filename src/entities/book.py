from sqlalchemy import (
  Column,
  String,
  Integer
)
from sqlalchemy.orm import relationship
from ..database.core import Base

class Libro(Base):
    __tablename__ = "libros"
    id = Column(Integer, primary_key=True, autoincrement=True)
    isbn = Column(String(20), unique=True, nullable=False)
    titulo = Column(String(200), nullable=False)
    autor = Column(String(100), nullable=False)
    num_paginas = Column(Integer)
    total_ejemplares = Column(Integer, default=0)
    portada_uri = Column(String(300))

    ejemplares = relationship("Ejemplar", back_populates="libro")
    recomendaciones_origen = relationship(
        "Recomendacion",
        back_populates="libro_origen",
        foreign_keys="Recomendacion.origen_id"
    )
    recomendaciones_destino = relationship(
        "Recomendacion",
        back_populates="libro_recomendado",
        foreign_keys="Recomendacion.recomendado_id"
    )