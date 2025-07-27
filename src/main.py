from fastapi import FastAPI, HTTPException, Depends
from .database.core import engine, Base

from .entities.user import Usuario
from .entities.teacher import Profesor
from .entities.student import Alumno
# from .entities.copyBook import 

from .api import register_routes
from .logging import configure_logging, LogLevels

configure_logging(LogLevels.info)

app = FastAPI()

Base.metadata.create_all(bind=engine)

register_routes(app)