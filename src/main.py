from fastapi import FastAPI, HTTPException, Depends
from .database.core import engine, Base
from .entities.copyBook import CopyBook

from .api import register_routes

app = FastAPI()
