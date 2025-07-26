from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from datetime import date
from ..database.core import Base

class Multa(Base):
    __tablename__ = "multas"
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    fecha_inicio = Column(Date, default=date.today)
    dias_acumulados = Column(Integer, default=0)
    fecha_fin = Column(Date)

    usuario = relationship("Usuario", back_populates="multas")
    prestamos_hist = relationship("PrestamoHist", back_populates="multa")
    multas_hist = relationship("MultaHist", back_populates="multa")
