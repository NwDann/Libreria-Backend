from enum import Enum 
from pydantic import BaseModel, EmailStr
from typing import Optional

class TipoUsuarioEnum(str, Enum):
    ALUMNO = "ALUMNO"
    PROFESOR = "PROFESOR"

class RegisterUserRequest(BaseModel):
    id: int
    password: str
    email: EmailStr
    nombre: str
    apellido1: str
    apellido2: Optional[str] = None
    ciudad: Optional[str] = None
    tipo: TipoUsuarioEnum  # 'alumno' o 'profesor'
    telefono_padres: Optional[str] = None  # Solo requerido si es alumno
    departamento: Optional[str] = None # Solo requerido si es profesor

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: int | None = None
