from sqlalchemy import (
  Column,
  String,
  ForeignKey,
  Integer
)
from user import Usuario

class Alumno(Usuario):
    __tablename__ = "alumnos"
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), primary_key=True)
    telefono_padres = Column(String(20), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "alumno",
    }