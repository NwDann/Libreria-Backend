from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from ..database.core import Base

class PrestamoHist(Base):
    __tablename__ = "prestamos_hist"
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    ejemplar_id = Column(Integer, ForeignKey("ejemplares.id"), nullable=False)
    fecha_prestamo = Column(Date, nullable=False)
    fecha_prevista = Column(Date, nullable=False)
    fecha_devolucion = Column(Date, nullable=False)
    multa_id = Column(Integer, ForeignKey("multas.id"))

    usuario = relationship("Usuario", back_populates="prestamos_hist")
    ejemplar = relationship("Ejemplar", back_populates="prestamos_hist")
    multa = relationship("Multa", back_populates="prestamos_hist")
