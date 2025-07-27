from sqlalchemy import Column, Integer, ForeignKey, Date
from datetime import date
from sqlalchemy.orm import relationship
from ..database.core import Base

class Prestamo(Base):
    __tablename__ = "prestamos"
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    ejemplar_id = Column(Integer, ForeignKey("ejemplares.id"), nullable=False)
    fecha_prestamo = Column(Date, nullable=False, default=date.today)
    fecha_prevista = Column(Date, nullable=False)

    usuario = relationship("Usuario", back_populates="prestamos")
    ejemplar = relationship("Ejemplar", back_populates="prestamos")