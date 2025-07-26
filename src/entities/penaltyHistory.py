from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from ..database.core import Base

class MultaHist(Base):
    __tablename__ = "multas_hist"
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    multa_id = Column(Integer, ForeignKey("multas.id"), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)

    usuario = relationship("Usuario", back_populates="multas_hist")
    multa = relationship("Multa", back_populates="multas_hist")
