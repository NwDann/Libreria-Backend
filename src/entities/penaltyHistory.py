from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from ..database.core import Base

class MultaHist(Base):
    __tablename__ = "multas_hist"
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    dias_acumulados = Column(Integer, default=0, nullable=False)
    fecha_fin = Column(Date, nullable=False)

    usuario = relationship("Usuario", back_populates="multas_hist")
    prestamos_hist = relationship("PrestamoHist", back_populates="multa")
    
