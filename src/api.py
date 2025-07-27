from fastapi import FastAPI
from src.auth.controller import router as auth_rt

from .controllers.book_ctr import router as book_rt
from .controllers.copyBook_ctr import router as copybook_rt
from .controllers.loan_ctr import router as loan_rt
from .controllers.loanHistory_ctr import router as loanh_rt
from .controllers.penalty_ctr import router as penalty_rt
from .controllers.penaltyHistory_ctr import router as penaltyH_rt
from .controllers.recomendation_ctr import router as recom_rt

def register_routes(app: FastAPI):
  app.include_router(auth_rt)
  app.include_router(book_rt)
  app.include_router(copybook_rt)
  app.include_router(loan_rt)
  app.include_router(loanh_rt)
  app.include_router(penalty_rt)
  app.include_router(penaltyH_rt)
  app.include_router(recom_rt)