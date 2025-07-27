from fastapi import FastAPI
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

Base.metadata.create_all(bind=engine)

register_routes(app)