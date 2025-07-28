from sqlalchemy import (
  Column,
  String,
  ForeignKey,
  BigInteger
)
from ..database.core import Base

class Alumno(Base):
    __tablename__ = "alumnos"
    usuario_id = Column(BigInteger, primary_key=True)
    telefono_padres = Column(String(20), nullable=False)