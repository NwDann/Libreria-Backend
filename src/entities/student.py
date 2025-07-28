from sqlalchemy import (
  Column,
  String,
  ForeignKey,
  BigInteger
)
from .user import Usuario

class Alumno(Usuario):
    __tablename__ = "alumnos"
    usuario_id = Column(BigInteger, ForeignKey("usuarios.id"), primary_key=True)
    telefono_padres = Column(String(20), nullable=False)