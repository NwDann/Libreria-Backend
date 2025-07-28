from datetime import timedelta, datetime, timezone
from typing import Annotated
from fastapi import Depends

from passlib.context import CryptContext
import jwt
from jwt import PyJWTError

from sqlalchemy.orm import Session
from src.entities.user import Usuario
from src.entities.student import Alumno
from src.entities.teacher import Profesor
from . import models

from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from ..exceptions import AuthenticationError
import logging

from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET-KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')
bcrypt_context = CryptContext(schemes=['argon2'], deprecated='auto')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return bcrypt_context.hash(password)


def authenticate_user(email: str, password: str, db: Session) -> Usuario | bool:
    user = db.query(Usuario).filter(Usuario.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        logging.warning(f"Intento de autenticacion fallida: {email}")
        return False
    return user


def create_access_token(email: str, user_id: int, expires_delta: timedelta) -> str:
    encode = {
        'sub': email,
        'id': str(user_id),
        'exp': datetime.now(timezone.utc) + expires_delta
    }
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> models.TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = int(payload.get('id'), 10)
        return models.TokenData(user_id=user_id)
    except PyJWTError as e:
        logging.warning(f"Verificacion fallida del token: {str(e)}")
        raise AuthenticationError()

def register_user(db: Session, register_user_request: models.RegisterUserRequest) -> None:
    try:
        if (register_user_request.telefono_padres is None and register_user_request.departamento is None) or (register_user_request.telefono_padres is not None and register_user_request.departamento is not None):
            raise AuthenticationError()
        print("Ahora un hash: ")
        password_hash =str(get_password_hash(register_user_request.password))
        print(password_hash)
        print(register_user_request.dict())
        print("Adioss")
        
        new_user = Usuario(
            id=register_user_request.id,
            email=register_user_request.email,
            nombre=register_user_request.nombre,
            apellido1=register_user_request.apellido1,
            apellido2=register_user_request.apellido2,
            ciudad=register_user_request.ciudad,
            tipo=register_user_request.tipo,
            password_hash=password_hash
        )    
        db.add(new_user)
        
        if register_user_request.tipo == models.TipoUsuarioEnum.ALUMNO:
            alumno = Alumno(
                usuario_id=register_user_request.id,
                telefono_padres=register_user_request.telefono_padres
            )
            db.add(alumno)
        elif register_user_request.tipo == models.TipoUsuarioEnum.PROFESOR:
            profesor = Profesor(
                usuario_id=register_user_request.id,
                departamento=register_user_request.departamento
            )
            db.add(profesor)
        
        db.commit()
        
    except Exception as e:
        db.rollback()
        logging.error(f"Error al registrar el usuario: {register_user_request.email}. Error: {str(e)}")
        raise

def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]) -> models.TokenData:
    return verify_token(token)

CurrentUser = Annotated[models.TokenData, Depends(get_current_user)]


def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: Session) -> models.Token:
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise AuthenticationError()
    token = create_access_token(user.email, user.id, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return models.Token(access_token=token, token_type='bearer')
