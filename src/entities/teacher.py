from sqlalchemy import (
  Column,
  String,
  ForeignKey,
  BigInteger
)
from ..database.core import Base

class Profesor(Base):
    __tablename__ = "profesores"
    usuario_id = Column(BigInteger, primary_key=True)
    departamento = Column(String(100), nullable=False)