from pydantic import BaseModel, EmailStr

class RegisterUserRequest(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str
    tipo: str  # 'alumno' o 'profesor'

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: int | None = None  # ID entero (no UUID)
