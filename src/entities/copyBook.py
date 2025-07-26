from sqlalchemy import (
  Column,
  ForeignKey,
  Date,
  String,
  Integer
)
from sqlalchemy.orm import relationship
from datetime import date
from ..database.core import Base

class Ejemplar(Base):
    __tablename__ = "ejemplares"
    id = Column(Integer, primary_key=True, autoincrement=True)
    libro_id = Column(Integer, ForeignKey("libros.id"), nullable=False)
    codigo = Column(String(50), unique=True, nullable=False)
    fecha_adquisicion = Column(Date, default=date.today)
    observaciones = Column(String(500), nullable=True)

    libro = relationship("Libro", back_populates="ejemplares")
    prestamos_hist = relationship("PrestamoHist", back_populates="ejemplar")