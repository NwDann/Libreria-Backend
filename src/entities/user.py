from sqlalchemy import (
  Column,
  String,
  Enum as PgEnum,
  Integer
)
from sqlalchemy.orm import relationship
from enum import Enum
from ..database.core import Base

class EstadoUsuarioEnum(str, Enum):
    ACTIVO = "ACTIVO"
    MOROSO = "MOROSO"
    MULTADO = "MULTADO"

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True)
    password_hash = Column(String(128), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    nombre = Column(String(50), nullable=False)
    apellido1 = Column(String(50), nullable=False)
    apellido2 = Column(String(50))
    ciudad = Column(String(50), nullable=False)
    estado = Column(PgEnum(EstadoUsuarioEnum), default=EstadoUsuarioEnum.ACTIVO, nullable=False)
    type = Column(String(20), nullable=False)  # para herencia

    __mapper_args__ = {
        "polymorphic_identity": "usuario",
        "polymorphic_on": type
    }

    prestamos_hist = relationship("PrestamoHist", back_populates="usuario")
    multas_hist = relationship("MultaHist", back_populates="usuario")