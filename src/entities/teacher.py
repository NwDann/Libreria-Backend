from sqlalchemy import (
  Column,
  String,
  ForeignKey,
  BigInteger
)
from .user import Usuario, TipoUsuarioEnum

class Profesor(Usuario):
    __tablename__ = "profesores"
    usuario_id = Column(BigInteger, ForeignKey("usuarios.id"), primary_key=True)
    departamento = Column(String(100), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": TipoUsuarioEnum.PROFESOR.value,
    }