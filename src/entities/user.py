from sqlalchemy import (
  Column,
  String,
  Enum as PgEnum,
  BigInteger
)
from sqlalchemy.orm import relationship
from enum import Enum
from ..database.core import Base

class EstadoUsuarioEnum(str, Enum):
    ACTIVO = "ACTIVO"
    MOROSO = "MOROSO"
    MULTADO = "MULTADO"

class TipoUsuarioEnum(str, Enum):
    ALUMNO = "ALUMNO"
    PROFESOR = "PROFESOR"

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(BigInteger, primary_key=True)
    password_hash = Column(String(260), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    nombre = Column(String(50), nullable=False)
    apellido1 = Column(String(50), nullable=False)
    apellido2 = Column(String(50), nullable=True)
    ciudad = Column(String(50), nullable=False)
    estado = Column(PgEnum(EstadoUsuarioEnum), default=EstadoUsuarioEnum.ACTIVO, nullable=False)
    tipo = Column(PgEnum(TipoUsuarioEnum), nullable=False)

    prestamos_hist = relationship("PrestamoHist", back_populates="usuario")
    multas_hist = relationship("MultaHist", back_populates="usuario")
    prestamos = relationship("Prestamo", back_populates="usuario")
    multas = relationship("Multa", back_populates="usuario")