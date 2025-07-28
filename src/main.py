from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database.core import engine, Base

from .entities.user import Usuario
from .entities.teacher import Profesor
from .entities.student import Alumno
from .entities.book import Libro
from .entities.copyBook import Ejemplar
from .entities.recomendation import Recomendacion
from .entities.loan import Prestamo
from .entities.loanHistory import PrestamoHist
from .entities.penalty import Multa
from .entities.penaltyHistory import MultaHist

from .api import register_routes
from .logging import configure_logging, LogLevels

configure_logging(LogLevels.info)

app = FastAPI()

origins = [
  "http://localhost:5173",
  "http://localhost:8000"
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"]
)

# Base.metadata.create_all(bind=engine)

register_routes(app)